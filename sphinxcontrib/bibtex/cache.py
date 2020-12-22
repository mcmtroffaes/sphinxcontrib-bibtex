# -*- coding: utf-8 -*-
"""
    Classes and methods to maintain any bibtex information that is stored
    outside the doctree.

    .. autoclass:: BibtexDomain
        :members:

    .. autoclass:: BibliographyCache
        :members:
"""

import ast
import collections
import copy
from typing import List, Dict, NamedTuple, Tuple, Set

import docutils.nodes
import re

from sphinx.addnodes import pending_xref
from sphinx.builders import Builder
from sphinx.domains import Domain
from sphinx.environment import BuildEnvironment
from sphinx.errors import ExtensionError

from .bibfile import BibfileCache, normpath_filename, process_bibfile


def _raise_invalid_node(node):
    """Helper method to raise an exception when an invalid node is
    visited.
    """
    raise ValueError("invalid node %s in filter expression" % node)


class _FilterVisitor(ast.NodeVisitor):

    """Visit the abstract syntax tree of a parsed filter expression."""

    entry = None
    """The bibliographic entry to which the filter must be applied."""

    cited_docnames = False
    """The documents where the entry is cited (empty if not cited)."""

    def __init__(self, entry, docname, cited_docnames):
        self.entry = entry
        self.docname = docname
        self.cited_docnames = cited_docnames

    def visit_Module(self, node):
        if len(node.body) != 1:
            raise ValueError(
                "filter expression cannot contain multiple expressions")
        return self.visit(node.body[0])

    def visit_Expr(self, node):
        return self.visit(node.value)

    def visit_BoolOp(self, node):
        outcomes = (self.visit(value) for value in node.values)
        if isinstance(node.op, ast.And):
            return all(outcomes)
        elif isinstance(node.op, ast.Or):
            return any(outcomes)
        else:  # pragma: no cover
            # there are no other boolean operators
            # so this code should never execute
            assert False, "unexpected boolean operator %s" % node.op

    def visit_UnaryOp(self, node):
        if isinstance(node.op, ast.Not):
            return not self.visit(node.operand)
        else:
            _raise_invalid_node(node)

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        op = node.op
        right = self.visit(node.right)
        if isinstance(op, ast.Mod):
            # modulo operator is used for regular expression matching
            if not isinstance(left, str):
                raise ValueError(
                    "expected a string on left side of %s" % node.op)
            if not isinstance(right, str):
                raise ValueError(
                    "expected a string on right side of %s" % node.op)
            return re.search(right, left, re.IGNORECASE)
        elif isinstance(op, ast.BitOr):
            return left | right
        elif isinstance(op, ast.BitAnd):
            return left & right
        else:
            _raise_invalid_node(node)

    def visit_Compare(self, node):
        # keep it simple: binary comparators only
        if len(node.ops) != 1:
            raise ValueError("syntax for multiple comparators not supported")
        left = self.visit(node.left)
        op = node.ops[0]
        right = self.visit(node.comparators[0])
        if isinstance(op, ast.Eq):
            return left == right
        elif isinstance(op, ast.NotEq):
            return left != right
        elif isinstance(op, ast.Lt):
            return left < right
        elif isinstance(op, ast.LtE):
            return left <= right
        elif isinstance(op, ast.Gt):
            return left > right
        elif isinstance(op, ast.GtE):
            return left >= right
        elif isinstance(op, ast.In):
            return left in right
        elif isinstance(op, ast.NotIn):
            return left not in right
        else:
            # not used currently: ast.Is | ast.IsNot
            _raise_invalid_node(op)

    def visit_Name(self, node):
        """Calculate the value of the given identifier."""
        id_ = node.id
        if id_ == 'type':
            return self.entry.type.lower()
        elif id_ == 'key':
            return self.entry.key.lower()
        elif id_ == 'cited':
            return bool(self.cited_docnames)
        elif id_ == 'docname':
            return self.docname
        elif id_ == 'docnames':
            return self.cited_docnames
        elif id_ == 'author' or id_ == 'editor':
            if id_ in self.entry.persons:
                return u' and '.join(
                    str(person)  # XXX needs fix in pybtex?
                    for person in self.entry.persons[id_])
            else:
                return u''
        else:
            return self.entry.fields.get(id_, "")

    def visit_Set(self, node):
        return frozenset(self.visit(elt) for elt in node.elts)

    # NameConstant is Python 3.4 only
    def visit_NameConstant(self, node):
        return node.value  # pragma: no cover

    # Constant is Python 3.6+ only
    # Since 3.8 Num, Str, Bytes, NameConstant and Ellipsis are just Constant
    def visit_Constant(self, node):
        return node.value

    # Not used on 3.8+
    def visit_Str(self, node):
        return node.s  # pragma: no cover

    def generic_visit(self, node):
        _raise_invalid_node(node)


class BibliographyCache(NamedTuple):
    """Contains information about a bibliography directive."""
    docname: str  #: Document name.
    bibfiles: List[str]  #: List of bib files for this directive.
    style: str  #: The pybtex style.
    list_: str  #: The list type.
    enumtype: str  #: The sequence type (for enumerated lists).
    start: int  #: The first ordinal of the sequence (for enumerated lists).
    labels: Dict[str, str]  #: Maps citation keys to their final labels.
    labelprefix: str  #: String prefix for pybtex generated labels.
    keyprefix: str  #: String prefix for citation keys.
    filter_: ast.AST  #: Parsed filter expression.


class BibtexDomain(Domain):

    """Global bibtex extension information cache."""

    name = 'cite'
    label = 'BibTeX Citations'
    data_version = 1

    @property
    def bibfiles(self) -> Dict[str, BibfileCache]:
        return self.data.setdefault('bibfiles', {})  # filename -> cache

    @property
    def bibliographies(self) -> Dict[str, BibliographyCache]:
        return self.data.setdefault('bibliographies', {})  # id -> cache

    #: key -> (docname, citation id)
    @property
    def citations(self) -> Dict[str, Tuple[str, str]]:
        return self.data.setdefault('citations', {})

    #: key -> docnames
    @property
    def citation_refs(self) -> Dict[str, Set[str]]:
        return self.data.setdefault(
            'citation_refs', collections.defaultdict(set))

    @property
    def enum_count(self) -> Dict[str, int]:
        return self.data.setdefault('enum_count', {})  # doc -> enum count

    def __init__(self, env: BuildEnvironment):
        super().__init__(env)
        # check config
        if env.app.config.bibtex_bibfiles is None:
            raise ExtensionError(
                "You must configure the bibtex_bibfiles setting")
        # update bib file information in the cache
        for bibfile in env.app.config.bibtex_bibfiles:
            process_bibfile(
                self.bibfiles,
                normpath_filename(env, "/" + bibfile),
                env.app.config.bibtex_encoding)

    def clear_doc(self, docname: str) -> None:
        for id_, bibcache in list(self.bibliographies.items()):
            if bibcache.docname == docname:
                del self.bibliographies[id_]
        for key, (doc, id_) in list(self.citations.items()):
            if doc == docname:
                del self.citations[key]
        for key, docnames in list(self.citation_refs.items()):
            if docnames == {docname}:
                del self.citation_refs[key]
            elif docname in docnames:
                docnames.remove(docname)
        self.enum_count.pop(docname, None)

    def merge_domaindata(self, docnames: List[str], otherdata: Dict) -> None:
        for id_, bibcache in otherdata['bibliographies'].items():
            if bibcache.docname in docnames:
                self.bibliographies[id_] = bibcache
        for docname in docnames:
            if docname in otherdata['enum_count']:
                self.enum_count[docname] = otherdata['enum_count'][docname]
        for key, (doc, id_) in otherdata['citations'].items():
            if doc in docnames:
                self.citations[key] = doc
        for key, data in otherdata['citation_refs'].items():
            citation_refs = self.citation_refs.setdefault(key, set())
            for docname in data:
                if docname in docnames:
                    citation_refs.add(docname)

    def resolve_xref(self, env: BuildEnvironment, fromdocname: str,
                     builder: Builder, typ: str, target: str,
                     node: pending_xref, contnode: docutils.nodes.Element
                     ) -> docutils.nodes.Element:
        keys = [key.strip() for key in target.split(',')]
        node = docutils.nodes.inline('', '', classes=['cite'])
        for key in keys:
            todocname, labelid = self.citations[key]
            refuri = builder.get_relative_uri(fromdocname, todocname)
            lrefuri = '#'.join([refuri, labelid])
            # TODO generate proper labels
            label = "[" + key + "]"
            node += docutils.nodes.reference(
                label, label, internal=True, refuri=lrefuri)
        return node

    def get_label_from_key(self, key):
        """Return label for the given key."""
        for bibcache in self.bibliographies.values():
            if key in bibcache.labels:
                return bibcache.labels[key]
        else:
            raise KeyError("%s not found" % key)

    def get_all_cited_keys(self, docnames):
        """Yield all citation keys for given *docnames* in order, then
        ordered by citation order.
        """
        for docname in docnames:
            for key, docs in self.citation_refs.items():
                if docname in docs:
                    yield key

    def _get_bibliography_entries(self, id_, warn):
        """Return filtered bibliography entries, sorted by occurrence
        in the bib file.
        """
        # get the information of this bibliography node
        bibcache = self.bibliographies[id_]
        # generate entries
        for bibfile in bibcache.bibfiles:
            data = self.bibfiles[bibfile].data
            for entry in data.entries.values():
                # beware: the prefix is not stored in the data
                # to allow reusing the data for multiple bibliographies
                key = bibcache.keyprefix + entry.key
                visitor = _FilterVisitor(
                    entry=entry,
                    docname=bibcache.docname,
                    cited_docnames=self.citation_refs.get(key, set()))
                try:
                    success = visitor.visit(bibcache.filter_)
                except ValueError as err:
                    warn("syntax error in :filter: expression; %s" % err)
                    # recover by falling back to the default
                    success = key in self.citation_refs
                if success:
                    # entries are modified in an unpickable way
                    # when formatting, so fetch a deep copy
                    # and return this copy with prefixed key
                    # we do not deep copy entry.collection because that
                    # consumes enormous amounts of memory
                    entry.collection = None
                    entry2 = copy.deepcopy(entry)
                    entry2.key = bibcache.keyprefix + entry.key
                    entry2.collection = data
                    entry.collection = data
                    yield entry2

    def get_bibliography_entries(self, id_, warn, docnames):
        """Return filtered bibliography entries, sorted by citation order."""
        # get entries, ordered by bib file occurrence
        entries = collections.OrderedDict(
            (entry.key, entry) for entry in
            self._get_bibliography_entries(id_=id_, warn=warn))
        # order entries according to which were cited first
        # first, we add all keys that were cited
        # then, we add all remaining keys
        sorted_entries = []
        for key in self.get_all_cited_keys(docnames):
            try:
                entry = entries.pop(key)
            except KeyError:
                pass
            else:
                sorted_entries.append(entry)
        sorted_entries += entries.values()
        return sorted_entries
