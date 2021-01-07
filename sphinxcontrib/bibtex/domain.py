"""
    Classes and methods to maintain any bibtex information that is stored
    outside the doctree.

    .. autoclass:: Citation
        :members:

    .. autoclass:: BibtexDomain
        :members:
"""

import ast
from typing import TYPE_CHECKING
from typing import List, Dict, NamedTuple, cast, Iterable, Tuple, Set

import docutils.frontend
import docutils.nodes
import docutils.parsers.rst
import docutils.utils
import sphinx.util
import re

from pybtex.plugin import find_plugin
from sphinx.domains import Domain
from sphinx.errors import ExtensionError
from sphinx.util.nodes import make_refnode

from .bibfile import BibFile, normpath_filename, process_bibfile

if TYPE_CHECKING:
    from pybtex.database import Entry
    from pybtex.style import FormattedEntry
    from pybtex.style.formatting import BaseStyle
    from sphinx.addnodes import pending_xref
    from sphinx.application import Sphinx
    from sphinx.builders import Builder
    from sphinx.environment import BuildEnvironment
    from .directives import BibliographyKey, BibliographyValue
    from .roles import CitationRef


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
    """Get document names in order."""
    rel = env.collect_relations()
    docname = env.config.master_doc
    docnames = set()
    while docname is not None:
        docnames.add(docname)
        yield docname
        parent, prevdoc, nextdoc = rel[docname]
        docname = nextdoc
    for docname in sorted(env.found_docs - docnames):
        yield docname


class Citation(NamedTuple):
    """Information about a citation."""
    citation_id: str                     #: Unique id of this citation.
    bibliography_key: "BibliographyKey"  #: Key of its bibliography directive.
    key: str                             #: Key (with prefix).
    label: str                           #: Label (with prefix).
    formatted_entry: "FormattedEntry"    #: Entry as formatted by pybtex.


def env_updated(app: "Sphinx", env: "BuildEnvironment") -> Iterable[str]:
    domain = cast(BibtexDomain, env.get_domain('cite'))
    return domain.env_updated()


class BibtexDomain(Domain):
    """Sphinx domain for the bibtex extension."""

    name = 'cite'
    label = 'BibTeX Citations'
    data_version = 3
    initial_data = dict(
        bibfiles={},
        bibliography_header=docutils.nodes.paragraph(),
        footbibliography_header=docutils.nodes.paragraph(),
        bibliographies={},
        citations=[],
        citation_refs=[],
    )

    @property
    def bibfiles(self) -> Dict[str, BibFile]:
        """Map each bib filename to some information about the file (including
        the parsed data).
        """
        return self.data['bibfiles']

    @property
    def bibliography_header(self) -> docutils.nodes.Element:
        return self.data['bibliography_header']

    @property
    def footbibliography_header(self) -> docutils.nodes.Element:
        return self.data['footbibliography_header']

    @property
    def bibliographies(self) -> Dict["BibliographyKey", "BibliographyValue"]:
        """Map storing information about each bibliography directive."""
        return self.data['bibliographies']

    @property
    def citations(self) -> List[Citation]:
        """Citation data."""
        return self.data['citations']

    @property
    def citation_refs(self) -> List["CitationRef"]:
        """Citation reference data."""
        return self.data['citation_refs']

    def __init__(self, env: "BuildEnvironment"):
        super().__init__(env)
        # connect env-updated
        env.app.connect('env-updated', env_updated)
        # check config
        if env.app.config.bibtex_bibfiles is None:
            raise ExtensionError(
                "You must configure the bibtex_bibfiles setting")
        # update bib file information in the cache
        for bibfile in env.app.config.bibtex_bibfiles:
            process_bibfile(
                self.bibfiles, normpath_filename(env, "/" + bibfile),
                env.app.config.bibtex_encoding)
        # parse bibliography headers
        for directive in ("bibliography", "footbibliography"):
            header = getattr(env.app.config, "bibtex_%s_header" % directive)
            if header:
                parser = docutils.parsers.rst.Parser()
                settings = docutils.frontend.OptionParser(
                    components=(docutils.parsers.rst.Parser,)
                ).get_default_values()
                document = docutils.utils.new_document(
                    "%s_header" % directive, settings)
                parser.parse(header, document)
                if len(document) > 0:
                    self.data["%s_header" % directive] = document[0]

    def clear_doc(self, docname: str) -> None:
        self.data['citations'] = [
            citation for citation in self.citations
            if citation.bibliography_key.docname != docname]
        self.data['citation_refs'] = [
            ref for ref in self.citation_refs if ref.docname != docname]
        for bib_key in list(self.bibliographies.keys()):
            if bib_key.docname == docname:
                del self.bibliographies[bib_key]

    def merge_domaindata(self, docnames: List[str], otherdata: Dict) -> None:
        for bib_key, bib_value in otherdata['bibliographies'].items():
            if bib_key.docname in docnames:
                self.bibliographies[bib_key] = bib_value
        for citation_ref in otherdata['citation_refs']:
            if citation_ref.docname in docnames:
                self.citation_refs.append(citation_ref)
        # 'citations' domain data calculated in env_updated

    def env_updated(self) -> Iterable[str]:
        # This function is called when all doctrees are parsed,
        # but before any post transforms are applied. We use it to
        # determine which citations will be added to which bibliography
        # directive, and also to format the labels. We need to format
        # the labels here because they must be known when resolve_xref is
        # called.
        self.citations.clear()  # might have been restored from pickle
        docnames = list(get_docnames(self.env))
        # we keep track of this to quickly check for duplicates
        used_keys: Set[str] = set()
        used_labels: Dict[str, str] = {}
        for bibliography_key, bibliography in self.bibliographies.items():
            for formatted_entry in self.get_formatted_entries(
                    bibliography_key, docnames):
                key = bibliography.keyprefix + formatted_entry.key
                label = bibliography.labelprefix + formatted_entry.label
                if bibliography.list_ == 'citation' and key in used_keys:
                    logger.warning(
                        'duplicate citation for key "%s"' % key,
                        location=(bibliography_key.docname, bibliography.line))
                self.citations.append(Citation(
                    citation_id=bibliography.citation_nodes[key]['ids'][0],
                    bibliography_key=bibliography_key,
                    key=key,
                    label=label,
                    formatted_entry=formatted_entry,
                ))
                if bibliography.list_ == 'citation':
                    used_keys.add(key)
                    if label not in used_labels:
                        used_labels[label] = key
                    elif used_labels[label] != key:
                        # if used_label[label] == key then already
                        # duplicate key warning
                        logger.warning(
                            'duplicate label "%s" for keys "%s" and "%s"' % (
                                label, used_labels[label], key),
                            location=(bibliography_key.docname,
                                      bibliography.line))
        return []  # expects list of updated docnames

    def resolve_xref(self, env: "BuildEnvironment", fromdocname: str,
                     builder: "Builder", typ: str, target: str,
                     node: "pending_xref", contnode: docutils.nodes.Element
                     ) -> docutils.nodes.Element:
        """Replace node by list of citation references (one for each key)."""
        keys = [key.strip() for key in target.split(',')]
        if builder.name != 'latex':
            citations_node = docutils.nodes.inline(rawsource=target, text='[')
        else:
            citations_node = docutils.nodes.inline(rawsource=target, text='')
        # map citation keys that can be resolved to their citation data
        citations = {
            cit.key: cit for cit in self.citations
            if cit.key in keys
            and self.bibliographies[cit.bibliography_key].list_ == 'citation'}
        for i, key in enumerate(keys):
            try:
                citation = citations[key]
            except KeyError:
                # TODO can handle missing reference warning using the domain
                logger.warning('could not find bibtex key "%s"' % key,
                               location=node)
                citations_node += docutils.nodes.inline('', key)
                continue
            refcontnode = docutils.nodes.inline('', citation.label)
            if builder.name == 'latex':
                # latex builder needs a citation_reference
                refnode = docutils.nodes.citation_reference(
                    '', refcontnode,
                    docname=citation.bibliography_key.docname,
                    refname=citation.citation_id)
            else:
                # other builders can use general reference node
                refnode = make_refnode(
                    builder, fromdocname,
                    citation.bibliography_key.docname,
                    citation.citation_id, refcontnode)
            citations_node += refnode
            if i != len(keys) - 1 and builder.name != 'latex':
                citations_node += docutils.nodes.Text(',')
        if builder.name != 'latex':
            citations_node += docutils.nodes.Text(']')
        return citations_node

    def get_all_cited_keys(self, docnames):
        """Yield all citation keys for given *docnames* in order, then
        ordered by citation order.
        """
        for citation_ref in sorted(
                self.citation_refs, key=lambda c: docnames.index(c.docname)):
            for key in citation_ref.keys:
                yield key

    def get_entries(
            self, bibfiles: List[str]) -> Iterable["Entry"]:
        """Return all bibliography entries from the bib files, unsorted (i.e.
        in order of appearance in the bib files.
        """
        for bibfile in bibfiles:
            for entry in self.bibfiles[bibfile].data.entries.values():
                yield entry

    def get_filtered_entries(
            self, bibliography_key: "BibliographyKey"
            ) -> Iterable[Tuple[str, "Entry"]]:
        """Return unsorted bibliography entries filtered by the filter
        expression.
        """
        bibliography = self.bibliographies[bibliography_key]
        for entry in self.get_entries(bibliography.bibfiles):
            key = bibliography.keyprefix + entry.key
            cited_docnames = {
                citation_ref.docname
                for citation_ref in self.citation_refs
                if key in citation_ref.keys
            }
            visitor = _FilterVisitor(
                entry=entry,
                docname=bibliography_key.docname,
                cited_docnames=cited_docnames)
            try:
                success = visitor.visit(bibliography.filter_)
            except ValueError as err:
                logger.warning(
                    "syntax error in :filter: expression; %s" % err,
                    location=(bibliography_key.docname, bibliography.line))
                # recover by falling back to the default
                success = bool(cited_docnames)
            if success:
                yield key, entry

    def get_sorted_entries(
            self, bibliography_key: "BibliographyKey", docnames: List[str]
            ) -> Iterable[Tuple[str, "Entry"]]:
        """Return filtered bibliography entries sorted by citation order."""
        entries = dict(
            self.get_filtered_entries(bibliography_key))
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

    def get_formatted_entries(
            self, bibliography_key: "BibliographyKey", docnames: List[str]
            ) -> Iterable["FormattedEntry"]:
        """Get sorted bibliography entries along with their pybtex labels,
        with additional sorting and formatting applied from the pybtex style.
        """
        bibliography = self.bibliographies[bibliography_key]
        entries = dict(
            self.get_sorted_entries(bibliography_key, docnames))
        style = cast("BaseStyle", find_plugin(
            'pybtex.style.formatting', bibliography.style)())
        return style.format_entries(entries.values())
