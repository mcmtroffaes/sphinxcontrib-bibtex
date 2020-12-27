"""
    .. autoclass:: FootCiteRole
        :show-inheritance:

        .. automethod:: result_nodes
"""

import docutils.nodes

from typing import cast, Optional, Tuple, List
from pybtex.plugin import find_plugin
from sphinx.environment import BuildEnvironment
from sphinx.roles import XRefRole

from .domain import BibtexDomain
from .bibfile import get_bibliography_entry


class FootCiteRole(XRefRole):
    """Class for processing the :rst:role:`footcite` role."""

    backend = find_plugin('pybtex.backends', 'docutils')()

    def make_refnode(self, document: docutils.nodes.document,
                     env: BuildEnvironment, key: str
                     ) -> Optional[docutils.nodes.footnote_reference]:
        domain = cast(BibtexDomain, self.env.get_domain('cite'))
        citation_refs = env.temp_data.setdefault(
            "bibtex_foot_citation_refs", {})
        for otherkeys in citation_refs.values():
            if key in otherkeys:
                entry = get_bibliography_entry(domain.bibfiles, key)
                assert entry is not None
                return self.backend.footnote_reference(entry, document)
        else:
            # note: keys is a dict used as an ordered set
            keys = citation_refs.setdefault(
                env.temp_data["bibtex_foot_bibliography_id"], {})
            entry = get_bibliography_entry(domain.bibfiles, key)
            if entry is not None:
                keys[key] = None
                return self.backend.footnote_reference(entry, document)
            else:
                return None

    def result_nodes(self, document: docutils.nodes.document,
                     env: BuildEnvironment, node: docutils.nodes.Element,
                     is_ref: bool
                     ) -> Tuple[List[docutils.nodes.Node],
                                List[docutils.nodes.system_message]]:
        """Transform reference node into a footnote reference,
        and note that the reference was cited.
        """
        keys = [key.strip() for key in self.target.split(',')]  # type: ignore
        refnodes = [self.make_refnode(document, env, key) for key in keys]
        return [refnode for refnode in refnodes if refnode is not None], []
