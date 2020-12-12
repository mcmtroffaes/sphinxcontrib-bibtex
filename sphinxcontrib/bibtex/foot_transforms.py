"""
    .. autoclass:: FootBibliographyTransform
        :show-inheritance:

        .. autoattribute:: default_priority
        .. automethod:: apply
"""

import docutils.nodes
import docutils.transforms
import sphinx.util
from pybtex.plugin import find_plugin
from .transforms import node_text_transform, transform_url_command
from .foot_nodes import footbibliography
from .bibfile import get_bibliography_entry


logger = sphinx.util.logging.getLogger(__name__)


class FootBibliographyTransform(docutils.transforms.Transform):

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
        env = self.document.settings.env
        for bibnode in self.document.traverse(footbibliography):
            id_ = bibnode['ids'][0]
            entries = [
                get_bibliography_entry(env.bibtex_cache.bibfiles, key)
                for key in env.bibtex_cache.foot_cited[env.docname][id_]]
            entries2 = [entry for entry in entries if entry is not None]
            # locate and instantiate style and backend plugins
            style = find_plugin(
                'pybtex.style.formatting',
                env.app.config.bibtex_default_style)()
            backend = find_plugin('pybtex.backends', 'docutils')()
            # create footnote nodes for all references
            footnotes = docutils.nodes.paragraph()
            # remind: style.format_entries modifies entries in unpickable way
            for entry in style.format_entries(entries2):
                footnote = backend.footnote(entry, self.document)
                node_text_transform(footnote, transform_url_command)
                footnotes += footnote
            if env.bibtex_footbibliography_header is not None:
                nodes = [env.bibtex_footbibliography_header.deepcopy(),
                         footnotes]
            else:
                nodes = footnotes
            bibnode.replace_self(nodes)
