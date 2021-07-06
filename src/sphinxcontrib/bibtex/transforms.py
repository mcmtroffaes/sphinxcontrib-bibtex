"""
    .. autoclass:: BibliographyTransform
        :show-inheritance:

        .. autoattribute:: default_priority
        .. automethod:: run

    .. autofunction:: node_text_transform

    .. autofunction:: transform_url_command
"""

import docutils.nodes

from typing import TYPE_CHECKING, cast
from pybtex.plugin import find_plugin
from sphinx.transforms.post_transforms import SphinxPostTransform
from sphinx.util.logging import getLogger

from .directives import BibliographyKey
from .nodes import bibliography as bibliography_node

if TYPE_CHECKING:
    from sphinx.environment import BuildEnvironment
    from .domain import BibtexDomain

logger = getLogger(__name__)


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
    backend = find_plugin('pybtex.backends', 'docutils')()

    def run(self, **kwargs):
        """Transform each
        :class:`~sphinxcontrib.bibtex.nodes.bibliography` node into a
        list of citations.
        """
        env = cast("BuildEnvironment", self.document.settings.env)
        domain = cast("BibtexDomain", env.get_domain('cite'))
        for bibnode in self.document.traverse(bibliography_node):
            # reminder: env.docname may be equal to 'index' instead of
            # bibnode['docname'] in post-transform phase (e.g. latex builder)
            bib_key = BibliographyKey(
                docname=bibnode['docname'], id_=bibnode['ids'][0])
            bibliography = domain.bibliographies[bib_key]
            citations = [citation for citation in domain.citations
                         if citation.bibliography_key == bib_key]
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
                nodes = []
            for citation in citations:
                citation_node = bibliography.citation_nodes[citation.key]
                if bibliography.list_ in {"enumerated", "bullet"}:
                    citation_node += self.backend.paragraph(
                        citation.formatted_entry)
                else:  # "citation"
                    # backrefs only supported in same document
                    backrefs = [
                        citation_ref.citation_ref_id
                        for citation_ref in domain.citation_refs
                        if bib_key.docname == citation_ref.docname
                        and citation.key in citation_ref.keys]
                    if backrefs:
                        citation_node['backrefs'] = backrefs
                    citation_node += docutils.nodes.label(
                        '', citation.formatted_entry.label,
                        support_smartquotes=False)
                    citation_node += self.backend.paragraph(
                        citation.formatted_entry)
                citation_node['docname'] = bib_key.docname
                node_text_transform(citation_node, transform_url_command)
                nodes.append(citation_node)
                if bibliography.list_ == "enumerated":
                    env.temp_data['bibtex_enum_count'] += 1
            if citations:
                final_node = domain.bibliography_header.deepcopy()
                final_node += nodes
                bibnode.replace_self(final_node)
            else:
                bibnode.replace_self(docutils.nodes.target())
