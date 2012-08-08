"""
    New Doctree Transforms
    ~~~~~~~~~~~~~~~~~~~~~~

    .. autoclass:: BibliographyTransform

        .. autoattribute:: default_priority
        .. automethod:: apply
"""

import copy
import docutils.nodes
import docutils.transforms

from pybtex.backends.doctree import Backend as output_backend
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
    """Convert '\\url{...}' into a proper docutils hyperlink."""
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
            info = [info for other_id, info
                    in env.bibtex_cache.bibliographies.iteritems()
                    if other_id == id_][0]
            # generate entries
            entries = []
            for bibfile in info.bibfiles:
                # XXX entries are modified below in an unpickable way
                # XXX so fetch a deep copy
                data = env.bibtex_cache.bibfiles[bibfile].data
                if info.cite == "all":
                    bibfile_entries = data.entries.itervalues()
                elif info.cite == "cited":
                    bibfile_entries = (
                        entry for entry in data.entries.itervalues()
                        if entry.key in env.bibtex_cited)
                elif info.cite == "notcited":
                    bibfile_entries = (
                        entry for entry in data.entries.itervalues()
                        if entry.key not in env.bibtex_cited)
                else:
                    raise RuntimeError("invalid cite option (%s)" % info.cite)
                entries += copy.deepcopy(list(bibfile_entries))
            # locate and instantiate style plugin
            style_cls = find_plugin(
                'pybtex.style.formatting', info.style)
            style = style_cls()
            # create citation nodes for all references
            backend = output_backend()
            if info.list_ == "enumerated":
                nodes = docutils.nodes.enumerated_list()
                nodes['enumtype'] = info.enumtype
                if info.start >= 1:
                    nodes['start'] = info.start
                    env.bibtex_enum_count = info.start
                else:
                    nodes['start'] = env.bibtex_enum_count
            elif info.list_ == "bullet":
                nodes = docutils.nodes.bullet_list()
            else: # "citation"
                nodes = docutils.nodes.paragraph()
            # XXX style.format_entries modifies entries in unpickable way
            for entry in style.format_entries(entries):
                if info.list_ == "enumerated" or info.list_ == "bullet":
                    citation = docutils.nodes.list_item()
                    citation += entry.text.render(backend)
                else: # "citation"
                    citation = backend.citation(entry, self.document)
                    label = citation[0].astext()
                    try:
                        num = env.bibtex_citation_label[label]
                    except KeyError:
                        num = str(len(env.bibtex_citation_label) + 1)
                        env.bibtex_citation_label[label] = num
                node_text_transform(citation, transform_url_command)
                if info.curly_bracket_strip:
                    node_text_transform(citation, transform_curly_bracket_strip)
                nodes += citation
                if info.list_ == "enumerated":
                    env.bibtex_enum_count += 1
            bibnode.replace_self(nodes)
