"""
    .. autoclass:: BibliographyTransform
        :show-inheritance:

        .. autoattribute:: default_priority
        .. automethod:: apply
"""

import docutils.nodes
import docutils.transforms

from pybtex.plugin import find_plugin

from ..bibtex.transforms import node_text_transform, transform_url_command
from .nodes import bibliography


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
        :class:`~sphinxcontrib.footbib.nodes.bibliography` node into a
        list of citations.
        """
        env = self.document.settings.env
        docname = env.docname
        for bibnode in self.document.traverse(bibliography):
            id_ = bibnode['ids'][0]
            entries = env.footbib_cache.get_bibliography_entries(
                docname, id_, env.bibtex_bibfiles)
            # locate and instantiate style and backend plugins
            style = find_plugin(
                'pybtex.style.formatting', env.app.config.bibtex_style)()
            backend = find_plugin('pybtex.backends', 'docutils')()
            # create citation nodes for all references
            nodes = docutils.nodes.paragraph()
            # remind: style.format_entries modifies entries in unpickable way
            for entry in style.format_entries(entries):
                footnote = backend.footnote(entry, self.document)
                node_text_transform(footnote, transform_url_command)
                nodes += footnote
            bibnode.replace_self(nodes)
