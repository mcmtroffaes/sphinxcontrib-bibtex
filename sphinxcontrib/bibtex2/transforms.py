"""
    .. autoclass:: BibliographyTransform
        :show-inheritance:

        .. autoattribute:: default_priority
        .. automethod:: apply
"""

import copy
import docutils.nodes
import docutils.transforms
import sphinx.util
from pybtex.plugin import find_plugin
from ..bibtex.transforms import node_text_transform, transform_url_command
from .nodes import bibliography


logger = sphinx.util.logging.getLogger(__name__)


def get_bibliography_entries(bibdatas, keys):
    """Return footnote bibliography entries from *bibfiles* for the
    given *keys*.
    """
    entries = []
    for key in keys:
        for data in bibdatas:
            try:
                entry = data.entries[key]
            except KeyError:
                pass
            else:
                # entries are modified in an unpickable way
                # when formatting, so fetch a deep copy
                # and return this copy
                # we do not deep copy entry.collection because that
                # consumes enormous amounts of memory
                entry.collection = None
                entry2 = copy.deepcopy(entry)
                entry2.key = entry.key
                entry2.collection = data
                entry.collection = data
                entries.append(entry)
                break
        else:
            logger.warning("could not find bibtex key {0}.".format(key))
    return entries


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
        for bibnode in self.document.traverse(bibliography):
            id_ = bibnode['ids'][0]
            bibdatas = [bibfile_cache.data
                        for bibfile_cache in env.bibtex_bibfiles.values()]
            keys = env.footbib_cache.cited[env.docname][id_]
            entries = get_bibliography_entries(bibdatas, keys)
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
