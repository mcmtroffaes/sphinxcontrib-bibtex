"""
    New Doctree Roles
    ~~~~~~~~~~~~~~~~~

    .. autoclass:: CiteRole
        :show-inheritance:

        .. automethod:: result_nodes
"""

from pybtex.plugin import find_plugin
import pybtex.database
from sphinx.roles import XRefRole


class CiteRole(XRefRole):

    """Class for processing the :rst:role:`footcite` role."""
    backend = find_plugin('pybtex.backends', 'docutils')()

    def result_nodes(self, document, env, node, is_ref):
        """Transform reference node into a footnote reference,
        and note that the reference was cited.
        """
        keys = node['reftarget'].split(',')
        # Note that at this point, usually, env.footbib_cache.bibfiles
        # is still empty because the bibliography directive may not
        # have been processed yet, so we cannot get the actual entry.
        # Instead, we simply fake an entry with the desired key.
        refnodes = [
            self.backend.footnote_reference(_fake_entry(key), document)
            for key in keys]
        for key in keys:
            env.footbib_cache.cited[env.docname].add(key)
        return refnodes, []


def _fake_entry(key):
    entry = pybtex.database.Entry(type_="")
    entry.key = key
    return entry
