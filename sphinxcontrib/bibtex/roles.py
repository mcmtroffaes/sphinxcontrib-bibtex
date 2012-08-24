"""
    New Doctree Roles
    ~~~~~~~~~~~~~~~~~

    .. autoclass:: CiteRole
        :show-inheritance:

        .. automethod:: result_nodes
"""

from pybtex.backends.doctree import Backend as output_backend
import pybtex.database
from sphinx.roles import XRefRole # for :cite:

class CiteRole(XRefRole):
    """Class for processing the :rst:role:`cite` role."""
    backend = output_backend()

    def result_nodes(self, document, env, node, is_ref):
        """Transform reference node into a citation reference,
        and note that the reference was cited.
        """
        key = node['reftarget']
        # find entry corresponding to key
        for cache in env.bibtex_cache.bibfiles.itervalues():
            if key in cache.data.entries:
                entry = cache.data.entries[key]
        else:
            # key not found: fake an entry
            entry = pybtex.database.Entry(type_=None)
            entry.key = key
        refnode = self.backend.citation_reference(entry, document)
        env.bibtex_cache.add_cited(key, env.docname)
        return [refnode], []
