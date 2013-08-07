"""
    New Doctree Transforms
    ~~~~~~~~~~~~~~~~~~~~~~

    .. autoclass:: BibliographyTransform
        :show-inheritance:

        .. autoattribute:: default_priority
        .. automethod:: apply

    .. autoclass:: FilterVisitor
        :members: entry, is_cited
        :show-inheritance:

    .. autofunction:: node_text_transform

    .. autofunction:: transform_curly_bracket_strip

    .. autofunction:: transform_url_command
"""

import sys
if sys.version_info < (2, 7):  # pragma: no cover
    from ordereddict import OrderedDict
else:                          # pragma: no cover
    from collections import OrderedDict

import ast
import re
import copy
import docutils.nodes
import docutils.transforms

from pybtex.plugin import find_plugin

from sphinxcontrib.bibtex.nodes import bibliography


def node_text_transform(node, transform):
    """Apply transformation to all Text nodes within node."""
    for child in node.children:
        if isinstance(child, docutils.nodes.Text):
            node.replace(child, transform(child))
        else:
            node_text_transform(child, transform)


def transform_curly_bracket_strip(textnode):
    """Strip curly brackets from text."""
    text = textnode.astext()
    if '{' in text or '}' in text:
        text = text.replace('{', '').replace('}', '')
        return docutils.nodes.Text(text)
    else:
        return textnode


def transform_url_command(textnode):
    """Convert '\\\\url{...}' into a proper docutils hyperlink."""
    text = textnode.astext()
    if '\\url' in text:
        text1, _, text = text.partition('\\url')
        text2, _, text3 = text.partition('}')
        text2 = text2.lstrip(' {')
        ref = docutils.nodes.reference(refuri=text2)
        ref += docutils.nodes.Text(text2)
        node = docutils.nodes.inline()
        node += transform_url_command(docutils.nodes.Text(text1))
        node += ref
        node += transform_url_command(docutils.nodes.Text(text3))
        return node
    else:
        return textnode


class FilterVisitor(ast.NodeVisitor):

    """Visit the abstract syntax tree of a parsed filter expression."""

    entry = None
    """The bibliographic entry to which the filter must be applied."""

    is_cited = False
    """Whether the entry is cited."""

    def _raise_invalid_node(self, node):
        """Helper method to raise an exception when an invalid node is
        visited.
        """
        raise ValueError("invalid node %s in filter expression" % node)

    def __init__(self, entry, is_cited):
        self.entry = entry
        self.is_cited = is_cited

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
            self._raise_invalid_node(node)

    def visit_BinOp(self, node):
        if isinstance(node.op, ast.Mod):
            # modulo operator is used for regular expression matching
            name = self.visit(node.left)
            regexp = self.visit(node.right)
            if not isinstance(name, basestring):
                raise ValueError(
                    "expected a string on left side of %s" % node.op)
            if not isinstance(regexp, basestring):
                raise ValueError(
                    "expected a string on right side of %s" % node.op)
            return re.search(regexp, name, re.IGNORECASE)
        else:
            self._raise_invalid_node(node)

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
        else:
            # not used currently: ast.Is | ast.IsNot | ast.In | ast.NotIn
            self._raise_invalid_node(op)

    def visit_Name(self, node):
        """Calculate the value of the given identifier."""
        id_ = node.id
        if id_ == 'type':
            return self.entry.type.lower()
        elif id_ == 'key':
            return self.entry.key.lower()
        elif id_ == 'cited':
            return self.is_cited
        elif id_ == 'True':
            return True
        elif id_ == 'False':
            return False
        elif id_ == 'author' or id_ == 'editor':
            if id_ in self.entry.persons:
                return u' and '.join(
                    unicode(person) for person in self.entry.persons[id_])
            else:
                return u''
        else:
            return self.entry.fields.get(id_, "")

    def visit_Str(self, node):
        return node.s

    def generic_visit(self, node):
        self._raise_invalid_node(node)


class BibliographyTransform(docutils.transforms.Transform):

    # transform must be applied before references are resolved
    default_priority = 10
    """Priority of the transform. See
    http://docutils.sourceforge.net/docs/ref/transforms.html
    """

    def apply(self):
        """Transform each
        :class:`~sphinxcontrib.bibtex.nodes.bibliography` node into a
        list of citations.
        """
        env = self.document.settings.env
        for bibnode in self.document.traverse(bibliography):
            # get the information of this bibliography node
            # by looking up its id in the bibliography cache
            id_ = bibnode['ids'][0]
            infos = [info for other_id, info
                     in env.bibtex_cache.bibliographies.iteritems()
                     if other_id == id_ and info.docname == env.docname]
            assert infos, "no bibliography id '%s' in %s" % (
                id_, env.docname)
            assert len(infos) == 1, "duplicate bibliography ids '%s' in %s" % (
                id_, env.docname)
            info = infos[0]
            # generate entries
            entries = OrderedDict()
            for bibfile in info.bibfiles:
                # XXX entries are modified below in an unpickable way
                # XXX so fetch a deep copy
                data = env.bibtex_cache.bibfiles[bibfile].data
                for entry in data.entries.itervalues():
                    visitor = FilterVisitor(
                        entry=entry,
                        is_cited=env.bibtex_cache.is_cited(entry.key))
                    try:
                        ok = visitor.visit(info.filter_)
                    except ValueError as e:
                        env.app.warn(
                            "syntax error in :filter: expression; %s" %
                            e)
                        # recover by falling back to the default
                        ok = env.bibtex_cache.is_cited(entry.key)
                    if ok:
                        entries[entry.key] = copy.deepcopy(entry)
            # order entries according to which were cited first
            # first, we add all keys that were cited
            # then, we add all remaining keys
            sorted_entries = []
            for key in env.bibtex_cache.get_all_cited_keys():
                try:
                    entry = entries.pop(key)
                except KeyError:
                    pass
                else:
                    sorted_entries.append(entry)
            sorted_entries += entries.itervalues()
            # locate and instantiate style and backend plugins
            style = find_plugin('pybtex.style.formatting', info.style)()
            backend = find_plugin('pybtex.backends', 'docutils')()
            # create citation nodes for all references
            if info.list_ == "enumerated":
                nodes = docutils.nodes.enumerated_list()
                nodes['enumtype'] = info.enumtype
                if info.start >= 1:
                    nodes['start'] = info.start
                    env.bibtex_cache.set_enum_count(env.docname, info.start)
                else:
                    nodes['start'] = env.bibtex_cache.get_enum_count(
                        env.docname)
            elif info.list_ == "bullet":
                nodes = docutils.nodes.bullet_list()
            else:  # "citation"
                nodes = docutils.nodes.paragraph()
            # XXX style.format_entries modifies entries in unpickable way
            for entry in style.format_entries(sorted_entries):
                if info.list_ == "enumerated" or info.list_ == "bullet":
                    citation = docutils.nodes.list_item()
                    citation += entry.text.render(backend)
                else:  # "citation"
                    citation = backend.citation(entry, self.document)
                    # backend.citation(...) uses entry.key as citation label
                    # we change it to entry.label later onwards
                    # but we must note the entry.label now;
                    # at this point, we also already prefix the label
                    key = citation[0].astext()
                    info.labels[key] = info.labelprefix + entry.label
                node_text_transform(citation, transform_url_command)
                if info.curly_bracket_strip:
                    node_text_transform(
                        citation,
                        transform_curly_bracket_strip)
                nodes += citation
                if info.list_ == "enumerated":
                    env.bibtex_cache.inc_enum_count(env.docname)
            bibnode.replace_self(nodes)
