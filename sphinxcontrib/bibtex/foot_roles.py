"""
    .. autoclass:: FootCiteRole
        :show-inheritance:

        .. automethod:: result_nodes
"""

from oset import oset

from pybtex.plugin import find_plugin
import pybtex.database
from sphinx.roles import XRefRole


class FootCiteRole(XRefRole):
    """Class for processing the :rst:role:`footcite` role."""

    backend = find_plugin('pybtex.backends', 'docutils')()

    def make_refnode(self, document, env, key):
        cited = env.temp_data.setdefault("bibtex_foot_cited", {})
        for otherkeys in cited.values():
            if key in otherkeys:
                break
        else:
            keys = cited.setdefault(
                env.temp_data["bibtex_foot_bibliography_id"], oset())
            keys.add(key)
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
