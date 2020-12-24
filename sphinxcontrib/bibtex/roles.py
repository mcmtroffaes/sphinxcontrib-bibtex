"""
    .. autoclass:: CiteRole
        :show-inheritance:

        .. automethod:: result_nodes
"""

from typing import cast

import docutils.nodes
from pybtex.plugin import find_plugin
import pybtex.database
from sphinx.roles import XRefRole

from .cache import BibtexDomain, CitationRef


class CiteRole(XRefRole):

    """Class for processing the :rst:role:`cite` role."""
    backend = find_plugin('pybtex.backends', 'docutils')()

    def result_nodes(self, document, env, node, is_ref):
        """Associate the pending_xref with the cite domain,
        and note the cited citation keys.
        """
        node['refdomain'] = 'cite'
        document.set_id(node, suggested_prefix='cite')
        domain = cast(BibtexDomain, env.get_domain('cite'))
        keys = [key.strip() for key in self.target.split(',')]
        domain.citation_refs.append(CitationRef(
            citation_ref_id=node['ids'][0],
            docname=env.docname,
            line=document.line,
            keys=keys,
        ))
        return [node], []
