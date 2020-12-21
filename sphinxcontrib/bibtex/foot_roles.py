"""
    .. autoclass:: FootCiteRole
        :show-inheritance:

        .. automethod:: result_nodes
"""
from typing import cast

from pybtex.plugin import find_plugin
import pybtex.database
from sphinx.roles import XRefRole

from .cache import BibtexDomain


class FootCiteRole(XRefRole):
    """Class for processing the :rst:role:`footcite` role."""

    backend = find_plugin('pybtex.backends', 'docutils')()

    def make_refnode(self, document, env, key):
        domain = cast(BibtexDomain, env.get_domain('cite'))
        cited = domain.foot_cited[env.docname]
        for otherkeys in cited.values():
            if key in otherkeys:
                break
        else:
            cited[domain.foot_current_id[env.docname]].add(key)
        # TODO get the actual entry
        return self.backend.footnote_reference(_fake_entry(key), document)

    def result_nodes(self, document, env, node, is_ref):
        """Transform reference node into a footnote reference,
        and note that the reference was cited.
        """
        keys = [key.strip() for key in node['reftarget'].split(',')]
        return [self.make_refnode(document, env, key) for key in keys], []


def _fake_entry(key):
    entry = pybtex.database.Entry(type_="")
    entry.key = key
    return entry
