"""
    .. autoclass:: CiteRole
        :show-inheritance:

        .. automethod:: result_nodes
"""
from typing import cast

from pybtex.plugin import find_plugin
import pybtex.database
from sphinx.roles import XRefRole

from .cache import BibtexDomain, CitationRef


class CiteRole(XRefRole):

    """Class for processing the :rst:role:`cite` role."""
    backend = find_plugin('pybtex.backends', 'docutils')()

    def result_nodes(self, document, env, node, is_ref):
        """Transform reference node into a citation reference,
        and note that the reference was cited.
        """
        node['refdomain'] = 'cite'
        domain = cast(BibtexDomain, env.get_domain('cite'))
        keys = [key.strip() for key in self.target.split(',')]
        for key in keys:
            citation_ref_id = 'bibtex-citation-ref-%s-%s' % (
                env.docname, env.new_serialno('bibtex'))
            domain.citation_refs.append(CitationRef(
                citation_ref_id=citation_ref_id,
                docname=env.docname,
                line=document.line,
                key=key,
            ))
        return [node], []


def _fake_entry(key):
    entry = pybtex.database.Entry(type_="")
    entry.key = key
    return entry
