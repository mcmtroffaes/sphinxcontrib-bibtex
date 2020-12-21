"""
    .. autoclass:: CiteRole
        :show-inheritance:

        .. automethod:: result_nodes
"""
from typing import cast

from pybtex.plugin import find_plugin
import pybtex.database
from sphinx.roles import XRefRole

from .cache import BibtexCitationDomain


class CiteRole(XRefRole):

    """Class for processing the :rst:role:`cite` role."""
    backend = find_plugin('pybtex.backends', 'docutils')()

    def result_nodes(self, document, env, node, is_ref):
        """Transform reference node into a citation reference,
        and note that the reference was cited.
        """
        keys = [key.strip() for key in node['reftarget'].split(',')]
        # Note that at this point, usually, env.bibtex_cache.bibfiles
        # is still empty because the bibliography directive may not
        # have been processed yet, so we cannot get the actual entry.
        # Instead, we simply fake an entry with the desired key, and
        # fix the label at doctree-resolved time. This happens in
        # process_citation_references.
        refnodes = [
            self.backend.citation_reference(_fake_entry(key), document)
            for key in keys]
        for refnode in refnodes:
            refnode['classes'].append('bibtex')
        domain = cast(BibtexCitationDomain, env.get_domain('cite'))
        for key in keys:
            domain.cited[env.docname].add(key)
        if key not in domain.cited_previous[env.docname]:
            env.note_reread()
        return refnodes, []


def _fake_entry(key):
    entry = pybtex.database.Entry(type_="")
    entry.key = key
    return entry
