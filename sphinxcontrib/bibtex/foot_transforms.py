"""
    .. autoclass:: FootBibliographyTransform
        :show-inheritance:

        .. autoattribute:: default_priority
        .. automethod:: apply
"""

from typing import cast

import docutils.nodes
from pybtex.plugin import find_plugin
from sphinx.transforms import SphinxTransform
from sphinx.util.logging import getLogger

from .domain import BibtexDomain
from .transforms import node_text_transform, transform_url_command
from .foot_nodes import footbibliography
from .bibfile import get_bibliography_entry


logger = getLogger(__name__)


class FootBibliographyTransform(SphinxTransform):

    """A docutils transform to generate footnotes for
    bibliography nodes.
    """

    # transform must be applied before references are resolved
    default_priority = 10
    """Priority of the transform. See
    https://docutils.sourceforge.io/docs/ref/transforms.html
    """

    def apply(self):
        """Transform each
        :class:`~sphinxcontrib.bibtex.foot_nodes.footbibliography` node into a
        list of citations.
        """
        for bibnode in self.document.traverse(footbibliography):
            domain = cast(BibtexDomain, self.env.get_domain('cite'))
            id_ = bibnode['ids'][0]
            keys = self.env.temp_data.get(
                "bibtex_foot_citation_refs", {}).get(id_, {})
            entries = [
                get_bibliography_entry(domain.bibfiles, key) for key in keys]
            assert None not in entries
            # locate and instantiate style and backend plugins
            style = find_plugin(
                'pybtex.style.formatting',
                self.config.bibtex_default_style)()
            backend = find_plugin('pybtex.backends', 'docutils')()
            # create footnote nodes for all references
            footnotes = docutils.nodes.paragraph()
            for entry in style.format_entries(entries):
                footnote = backend.footnote(entry, self.document)
                node_text_transform(footnote, transform_url_command)
                footnotes += footnote
            if self.env.bibtex_footbibliography_header is not None:
                footnotes = [
                    self.env.bibtex_footbibliography_header.deepcopy(),
                    footnotes]
            bibnode.replace_self(footnotes)
