"""
    .. autoclass:: BibliographyTransform
        :show-inheritance:

        .. autoattribute:: default_priority
        .. automethod:: run

    .. autofunction:: node_text_transform

    .. autofunction:: transform_url_command
"""
from typing import cast

import docutils.nodes
import docutils.transforms
import sphinx.util

from pybtex.plugin import find_plugin
from sphinx.transforms.post_transforms import SphinxPostTransform

from .bibfile import get_bibliography_entry
from .cache import BibtexDomain
from .nodes import bibliography


logger = sphinx.util.logging.getLogger(__name__)


def node_text_transform(node, transform):
    """Apply transformation to all Text nodes within node."""
    for child in node.children:
        if isinstance(child, docutils.nodes.Text):
            node.replace(child, transform(child))
        else:
            node_text_transform(child, transform)


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


class BibliographyTransform(SphinxPostTransform):
    """A docutils transform to generate citation entries for
    bibliography nodes.
    """

    # transform must be applied before sphinx runs its ReferencesResolver
    # which has priority 10, so when ReferencesResolver calls the cite domain
    # resolve_xref, the target is present and all will work fine
    default_priority = 5

    def run(self, **kwargs):
        """Transform each
        :class:`~sphinxcontrib.bibtex.nodes.bibliography` node into a
        list of citations.
        """
        env = self.document.settings.env
        domain = cast(BibtexDomain, env.get_domain('cite'))
        for bibnode in self.document.traverse(bibliography):
            bibliography_id = bibnode['ids'][0]
            bibcache = domain.bibliographies[bibliography_id]
            citations = {
                id_: citation
                for id_, citation in domain.citations.items()
                if citation.bibliography_id == bibliography_id}
            # locate and instantiate style and backend plugins
            style = find_plugin('pybtex.style.formatting', bibcache.style)()
            backend = find_plugin('pybtex.backends', 'docutils')()
            # create citation nodes for all references
            if bibcache.list_ == "enumerated":
                nodes = docutils.nodes.enumerated_list()
                nodes['enumtype'] = bibcache.enumtype
                if bibcache.start >= 1:
                    nodes['start'] = bibcache.start
                    domain.enum_count[env.docname] = bibcache.start
                else:
                    nodes['start'] = domain.enum_count[env.docname]
            elif bibcache.list_ == "bullet":
                nodes = docutils.nodes.bullet_list()
            else:  # "citation"
                nodes = docutils.nodes.paragraph()
            for citation_id, citation in citations.items():
                entry = style.format_entry(
                    citation.entry_label,
                    get_bibliography_entry(
                        domain.bibfiles, citation.entry_key))
                if bibcache.list_ in ["enumerated", "bullet"]:
                    citation_node = docutils.nodes.list_item()
                    citation_node += backend.paragraph(entry)
                else:  # "citation"
                    citation_node = docutils.nodes.citation()
                    citation_node += docutils.nodes.label('', citation.label)
                    citation_node += backend.paragraph(entry)
                    citation_node['ids'].append(citation_id)
                node_text_transform(citation_node, transform_url_command)
                nodes += citation_node
                if bibcache.list_ == "enumerated":
                    domain.enum_count[env.docname] += 1
            if env.bibtex_bibliography_header is not None:
                nodes = [env.bibtex_bibliography_header.deepcopy(), nodes]
            bibnode.replace_self(nodes)
