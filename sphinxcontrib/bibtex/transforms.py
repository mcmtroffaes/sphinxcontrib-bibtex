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
from .domain import BibtexDomain
from .nodes import bibliography as bibliography_node


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
        for bibnode in self.document.traverse(bibliography_node):
            bibliography_id = bibnode['ids'][0]
            bibliography = domain.bibliographies[bibliography_id]
            citations = [citation for citation in domain.citations
                         if citation.bibliography_id == bibliography_id]
            # locate and instantiate style and backend plugins
            style = find_plugin(
                'pybtex.style.formatting', bibliography.style)()
            backend = find_plugin('pybtex.backends', 'docutils')()
            # create citation nodes for all references
            if bibliography.list_ == "enumerated":
                nodes = docutils.nodes.enumerated_list()
                nodes['enumtype'] = bibliography.enumtype
                if bibliography.start >= 1:
                    nodes['start'] = bibliography.start
                    env.temp_data['bibtex_enum_count'] = bibliography.start
                else:
                    nodes['start'] = env.temp_data.setdefault(
                        'bibtex_enum_count', 1)
            elif bibliography.list_ == "bullet":
                nodes = docutils.nodes.bullet_list()
            else:  # "citation"
                nodes = docutils.nodes.paragraph()
            for citation in citations:
                entry = style.format_entry(
                    citation.entry_label,
                    get_bibliography_entry(
                        domain.bibfiles, citation.entry_key))
                if bibliography.list_ in ["enumerated", "bullet"]:
                    citation_node = docutils.nodes.list_item()
                    citation_node += backend.paragraph(entry)
                else:  # "citation"
                    citation_node = docutils.nodes.citation()
                    # backrefs only supported in same document
                    backrefs = [
                        citation_ref.citation_ref_id
                        for citation_ref in domain.citation_refs
                        if env.docname == citation_ref.docname
                        and citation.key in citation_ref.keys]
                    if backrefs:
                        citation_node['backrefs'] = backrefs
                    citation_node += docutils.nodes.label(
                        '', citation.label, support_smartquotes=False)
                    citation_node += backend.paragraph(entry)
                citation_node['docname'] = env.docname
                if citation.citation_id is not None:
                    citation_node['ids'].append(citation.citation_id)
                    citation_node['names'].append(citation.citation_id)
                node_text_transform(citation_node, transform_url_command)
                nodes.append(citation_node)
                if bibliography.list_ == "enumerated":
                    env.temp_data['bibtex_enum_count'] += 1
            if env.bibtex_bibliography_header is not None:
                nodes = [env.bibtex_bibliography_header.deepcopy(), nodes]
            bibnode.replace_self(nodes)
