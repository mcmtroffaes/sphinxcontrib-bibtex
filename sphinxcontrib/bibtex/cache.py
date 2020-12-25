# -*- coding: utf-8 -*-
"""
    Classes and methods to maintain any bibtex information that is stored
    outside the doctree.

    .. autoclass:: Bibliography
        :members:

    .. autoclass:: Citation
        :members:

    .. autoclass:: CitationRef
        :members:

    .. autoclass:: BibtexDomain
        :members:
"""

import ast
from typing import List, Dict, NamedTuple, cast, Optional, Iterable, Tuple

import docutils.nodes
import sphinx.util
import re

from pybtex.database import Entry
from pybtex.plugin import find_plugin
import pybtex.style.formatting
from sphinx.addnodes import pending_xref
from sphinx.builders import Builder
from sphinx.domains import Domain
from sphinx.environment import BuildEnvironment
from sphinx.errors import ExtensionError
from sphinx.util.nodes import make_refnode

from .bibfile import BibfileCache, normpath_filename, process_bibfile

logger = sphinx.util.logging.getLogger(__name__)


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


def get_docnames(env):
    """Ged document names in order."""
    rel = env.collect_relations()
    docname = env.config.master_doc
    while docname is not None:
        yield docname
        parent, prevdoc, nextdoc = rel[docname]
        docname = nextdoc


class Bibliography(NamedTuple):
    """Contains information about a bibliography directive."""
    docname: str         #: Document name.
    line: int            #: Line number of the directive in the document.
    bibfiles: List[str]  #: List of bib files for this directive.
    style: str           #: The pybtex style.
    list_: str           #: The list type.
    enumtype: str        #: The sequence type (for enumerated lists).
    start: int           #: The start of the sequence (for enumerated lists).
    labelprefix: str     #: String prefix for pybtex generated labels.
    keyprefix: str       #: String prefix for citation keys.
    filter_: ast.AST     #: Parsed filter expression.


class Citation(NamedTuple):
    """Information about a citation."""
    citation_id: Optional[str]   #: Unique id of this citation.
    bibliography_id: str         #: Unique id of its bibliography directive.
    key: str                     #: Unique citation id used for referencing.
    label: str                   #: Label (with brackets and label prefix).
    entry_key: str               #: The original key (no prefix).
    entry_label: str             #: The original label (no brackets or prefix).


class CitationRef(NamedTuple):
    """Information about a citation reference."""
    citation_ref_id: str  #: Unique id of this citation reference.
    docname: str          #: Document name.
    line: int             #: Line number.
    keys: List[str]       #: Citation keys (including key prefix).


class BibtexDomain(Domain):

    """Global bibtex extension information cache."""

    name = 'cite'
    label = 'BibTeX Citations'
    data_version = 1

    @property
    def bibfiles(self) -> Dict[str, BibfileCache]:
        """Map each bib filename to some information about the file (including
        the parsed data).
        """
        return self.data.setdefault('bibfiles', {})  # filename -> cache

    @property
    def bibliographies(self) -> Dict[str, Bibliography]:
        """Map each bibliography directive id to further information about the
        directive.
        """
        return self.data.setdefault('bibliographies', {})  # id -> cache

    @property
    def citations(self) -> List[Citation]:
        """Citation data."""
        return self.data.setdefault('citations', [])

    @property
    def citation_refs(self) -> List[CitationRef]:
        """Citation reference data."""
        return self.data.setdefault('citation_refs', [])

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
        self.data['citations'] = [
            citation for citation in self.citations
            if self.bibliographies[
                   citation.bibliography_id].docname != docname]
        self.data['citation_refs'] = [
            ref for ref in self.citation_refs
            if ref.docname != docname]
        for id_, bibcache in list(self.bibliographies.items()):
            if bibcache.docname == docname:
                del self.bibliographies[id_]

    def merge_domaindata(self, docnames: List[str], otherdata: Dict) -> None:
        for id_, bibcache in otherdata['bibliographies'].items():
            if bibcache.docname in docnames:
                self.bibliographies[id_] = bibcache
        for citation_ref in otherdata['citation_refs']:
            if citation_ref.docname in docnames:
                self.citation_refs.append(citation_ref)
        # citations created during check_consistency so never pickled
        assert not self.citations
        assert not otherdata['citations']

    def check_consistency(self) -> None:
        # This function is called when all doctrees are parsed,
        # but before any post transforms are applied. We use it to
        # determine which citations will be added to which bibliography
        # directive, and also to format the labels. We need to format
        # the labels and construct the citation ids here because they must be
        # known when resolve_xref is called.
        docnames = list(get_docnames(self.env))
        # we keep track of this to quickly check for duplicates
        used_keys = set()
        used_labels = {}
        used_ids = set()
        for bibliography_id, bibcache in self.bibliographies.items():
            for entry_label, entry in self.get_labelled_bibliography_entries(
                    bibcache, docnames):
                key = bibcache.keyprefix + entry.key
                label = bibcache.labelprefix + entry_label
                if bibcache.list_ != 'citation':
                    # no warning in this case, just don't generate link
                    citation_id = None
                elif key in used_keys:
                    logger.warning(
                        'duplicate citation for key %s' % key,
                        location=(bibcache.docname, bibcache.line))
                    # no id for this one
                    citation_id = None
                else:
                    base_id = 'bibtex-citation-{}'.format(
                        docutils.nodes.make_id(key))
                    if base_id not in used_ids:
                        citation_id = base_id
                    else:
                        num = 1
                        while base_id + str(num) in used_ids:
                            num += 1
                        citation_id = base_id + str(num)
                self.citations.append(Citation(
                    citation_id=citation_id,
                    bibliography_id=bibliography_id,
                    key=key,
                    label=label,
                    entry_key=entry.key,
                    entry_label=entry_label,
                ))
                used_keys.add(key)
                used_labels.setdefault(label, set()).add(key)
                used_ids.add(citation_id)
        for label, keys in used_labels.items():
            if len(keys) > 1:
                logger.warning(
                    'duplicate label %s for keys %s' % (
                        label, keys))

    def resolve_xref(self, env: BuildEnvironment, fromdocname: str,
                     builder: Builder, typ: str, target: str,
                     node: pending_xref, contnode: docutils.nodes.Element
                     ) -> docutils.nodes.Element:
        """Replace node by list of citation references (one for each key)."""
        keys = [key.strip() for key in target.split(',')]
        node = docutils.nodes.inline('', '', classes=['cite'])
        # map citation keys that can be resolved to their citation data
        citations = {
            cit.key: cit for cit in self.citations
            if cit.key in keys
            and self.bibliographies[cit.bibliography_id].list_ == 'citation'}
        for key in keys:
            try:
                citation = citations[key]
            except KeyError:
                # TODO can handle missing reference warning using the domain
                logger.warning('could not find bibtex key %s' % key)
                node += docutils.nodes.Text(key)
                continue
            if builder.name == 'latex':
                # latex builder needs a citation_reference
                refnode = docutils.nodes.citation_reference(
                    '', citation.label,
                    docname=env.docname,
                    refname=citation.citation_id)
            else:
                # other builders can use general reference node
                refcontnode = docutils.nodes.Text('[' + citation.label + ']')
                refnode = make_refnode(
                    builder, env.docname,
                    self.bibliographies[citation.bibliography_id].docname,
                    citation.citation_id, refcontnode)
            node += refnode
        return node

    def get_all_cited_keys(self, docnames):
        """Yield all citation keys for given *docnames* in order, then
        ordered by citation order.
        """
        for citation_ref in sorted(
                self.citation_refs, key=lambda c: docnames.index(c.docname)):
            for key in citation_ref.keys:
                yield key

    def get_bibliography_entries(
            self, bibliography: Bibliography) -> Iterable[Tuple[str, Entry]]:
        """Return all bibliography entries from the bib files."""
        for bibfile in bibliography.bibfiles:
            for entry in self.bibfiles[bibfile].data.entries.values():
                yield bibliography.keyprefix + entry.key, entry

    def get_filtered_bibliography_entries(
            self, bibliography: Bibliography) -> Iterable[Tuple[str, Entry]]:
        """Return filtered bibliography entries."""
        for key, entry in self.get_bibliography_entries(bibliography):
            key = bibliography.keyprefix + entry.key
            cited_docnames = {
                citation_ref.docname
                for citation_ref in self.citation_refs
                if key in citation_ref.keys
            }
            visitor = _FilterVisitor(
                entry=entry,
                docname=bibliography.docname,
                cited_docnames=cited_docnames)
            try:
                success = visitor.visit(bibliography.filter_)
            except ValueError as err:
                logger.warning(
                    "syntax error in :filter: expression; %s" % err,
                    location=(bibliography.docname, bibliography.line))
                # recover by falling back to the default
                success = bool(cited_docnames)
            if success:
                yield key, entry

    def get_sorted_bibliography_entries(
            self, bibliography: Bibliography, docnames: List[str]
            ) -> Iterable[Tuple[str, Entry]]:
        """Return sorted bibliography entries."""
        entries = dict(self.get_filtered_bibliography_entries(bibliography))
        # yield entries which were cited first, in citation order
        for key in self.get_all_cited_keys(docnames):
            try:
                entry = entries.pop(key)
            except KeyError:
                pass
            else:
                yield key, entry
        # then all remaining keys, in order of bibliography file
        for key, entry in entries.items():
            yield key, entry

    def get_labelled_bibliography_entries(
            self, bibliography: Bibliography, docnames: List[str]
            ) -> Iterable[Tuple[str, Entry]]:
        entries = dict(
            self.get_sorted_bibliography_entries(bibliography, docnames))
        style = cast(
            pybtex.style.formatting.BaseStyle,
            find_plugin('pybtex.style.formatting', bibliography.style)())
        sorted_entries = style.sort(entries.values())
        labels = style.format_labels(sorted_entries)
        return zip(labels, sorted_entries)
