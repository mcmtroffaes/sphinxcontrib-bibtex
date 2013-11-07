"""
    New Doctree Transforms
    ~~~~~~~~~~~~~~~~~~~~~~

    .. autoclass:: BibliographyTransform
        :show-inheritance:

        .. autoattribute:: default_priority
        .. automethod:: apply

    .. autofunction:: node_text_transform

    .. autofunction:: transform_curly_bracket_strip

    .. autofunction:: transform_url_command
"""

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


class BibliographyTransform(docutils.transforms.Transform):

    """A docutils transform to generate citation entries for
    bibliography nodes.
    """

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
        docname = env.docname
        for bibnode in self.document.traverse(bibliography):
            id_ = bibnode['ids'][0]
            bibcache = env.bibtex_cache.get_bibliography_cache(
                docname=docname, id_=id_)
            entries = env.bibtex_cache.get_bibliography_entries(
                docname=docname, id_=id_, warn=env.app.warn)
            # locate and instantiate style and backend plugins
            style = find_plugin('pybtex.style.formatting', bibcache.style)()
            backend = find_plugin('pybtex.backends', 'docutils')()
            # create citation nodes for all references
            if bibcache.list_ == "enumerated":
                nodes = docutils.nodes.enumerated_list()
                nodes['enumtype'] = bibcache.enumtype
                if bibcache.start >= 1:
                    nodes['start'] = bibcache.start
                    env.bibtex_cache.set_enum_count(
                        env.docname, bibcache.start)
                else:
                    nodes['start'] = env.bibtex_cache.get_enum_count(
                        env.docname)
            elif bibcache.list_ == "bullet":
                nodes = docutils.nodes.bullet_list()
            else:  # "citation"
                nodes = docutils.nodes.paragraph()
            # remind: style.format_entries modifies entries in unpickable way
            for entry in style.format_entries(entries):
                if bibcache.list_ in ["enumerated", "bullet"]:
                    citation = docutils.nodes.list_item()
                    citation += backend.paragraph(entry)
                else:  # "citation"
                    citation = backend.citation(entry, self.document)
                    # backend.citation(...) uses entry.key as citation label
                    # we change it to entry.label later onwards
                    # but we must note the entry.label now;
                    # at this point, we also already prefix the label
                    key = citation[0].astext()
                    bibcache.labels[key] = bibcache.labelprefix + entry.label
                node_text_transform(citation, transform_url_command)
                if bibcache.curly_bracket_strip:
                    node_text_transform(
                        citation,
                        transform_curly_bracket_strip)
                nodes += citation
                if bibcache.list_ == "enumerated":
                    env.bibtex_cache.inc_enum_count(env.docname)
            bibnode.replace_self(nodes)
