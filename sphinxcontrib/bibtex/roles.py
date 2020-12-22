"""
    .. autoclass:: CiteRole
        :show-inheritance:

        .. automethod:: result_nodes
"""
from typing import cast

from pybtex.plugin import find_plugin
import pybtex.database
from sphinx.addnodes import pending_xref
from sphinx.roles import XRefRole

from .cache import BibtexDomain


class CiteRole(XRefRole):

    """Class for processing the :rst:role:`cite` role."""
    backend = find_plugin('pybtex.backends', 'docutils')()

    def result_nodes(self, document, env, node, is_ref):
        """Transform reference node into a citation reference,
        and note that the reference was cited.
        """
        domain = cast(BibtexDomain, env.get_domain('cite'))
        refnodes = []
        for key in self.target.split(','):
            key = key.strip()
            refnode = pending_xref(
                key, refdomain='cite', reftype='citation',
                reftarget="bibtex-citation-%s" % key, refdoc=env.docname)
            domain.citation_refs[key].add(env.docname)
            refnodes += refnode
        return refnodes, []


def _fake_entry(key):
    entry = pybtex.database.Entry(type_="")
    entry.key = key
    return entry
