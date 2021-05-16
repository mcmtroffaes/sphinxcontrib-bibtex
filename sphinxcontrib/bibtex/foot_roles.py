"""
    .. autoclass:: FootCiteRole
        :show-inheritance:

        .. automethod:: result_nodes
"""

from typing import TYPE_CHECKING, cast, Tuple, List, NamedTuple

import docutils.nodes
import pybtex_docutils
from pybtex.plugin import find_plugin
from sphinx.roles import XRefRole
from sphinx.util.logging import getLogger

from .bibfile import get_bibliography_entry
from .richtext import BaseReferenceText
from .style.referencing import format_references
from .transforms import node_text_transform, transform_url_command

if TYPE_CHECKING:
    from sphinx.environment import BuildEnvironment
    from .domain import BibtexDomain
    from .foot_domain import BibtexFootDomain
    from pybtex.backends import BaseBackend

logger = getLogger(__name__)


class FootReferenceInfo(NamedTuple):
    """Tuple containing reference info to enable sphinx to resolve a footnote
    reference.
    """
    key: str                             #: Citation key.
    document: "docutils.nodes.document"  #: Current docutils document.


class FootReferenceText(BaseReferenceText[FootReferenceInfo]):
    """Pybtex rich text class for footnote references with the docutils
    backend, for use with :class:`SphinxReferenceInfo`.
    """

    def render(self, backend: "BaseBackend"):
        assert isinstance(backend, pybtex_docutils.Backend), \
               "FootReferenceText only supports the docutils backend"
        info = self.info[0]
        # see docutils.parsers.rst.states.Body.footnote_reference()
        refname = docutils.nodes.fully_normalize_name(info.key)
        refnode = docutils.nodes.footnote_reference(
            '[#%s]_' % info.key, refname=refname, auto=1)
        info.document.note_autofootnote_ref(refnode)
        info.document.note_footnote_ref(refnode)
        return [refnode]


class FootCiteRole(XRefRole):
    """Class for processing the :rst:role:`footcite` role."""

    def result_nodes(self, document: "docutils.nodes.document",
                     env: "BuildEnvironment", node: "docutils.nodes.Element",
                     is_ref: bool
                     ) -> Tuple[List["docutils.nodes.Node"],
                                List["docutils.nodes.system_message"]]:
        """Transform node into footnote references, and
        add footnotes to a node stored in the environment's temporary data
        if they are not yet present.

        .. seealso::

           The node containing all footnotes is inserted into the document by
           :meth:`.foot_directives.FootBibliographyDirective.run`.
        """
        if not node.get('refdomain'):
            assert node['reftype'] == 'footcite'
            node['refdomain'] = 'footcite'
            node['reftype'] = 'p'
        foot_domain = cast("BibtexFootDomain", self.env.get_domain('footcite'))
        keys = [key.strip() for key in self.target.split(',')]  # type: ignore
        try:
            foot_bibliography = env.temp_data["bibtex_foot_bibliography"]
        except KeyError:
            env.temp_data["bibtex_foot_bibliography"] = foot_bibliography = \
                foot_domain.bibliography_header.deepcopy()
        foot_old_refs = env.temp_data.setdefault("bibtex_foot_old_refs", set())
        foot_new_refs = env.temp_data.setdefault("bibtex_foot_new_refs", set())
        style = find_plugin(
            'pybtex.style.formatting',
            self.config.bibtex_default_style)()
        references = []
        domain = cast("BibtexDomain", self.env.get_domain('cite'))
        for key in keys:
            entry = get_bibliography_entry(domain.bibfiles, key)
            if entry is not None:
                formatted_entry = style.format_entry(label='', entry=entry)
                references.append(
                    (entry, formatted_entry,
                     FootReferenceInfo(key=entry.key, document=document)))
                if key not in (foot_old_refs | foot_new_refs):
                    footnote = domain.backend.footnote(
                        formatted_entry, document)
                    node_text_transform(footnote, transform_url_command)
                    foot_bibliography += footnote
                    foot_new_refs.add(key)
            else:
                logger.warning('could not find bibtex key "%s"' % key,
                               location=(env.docname, self.lineno))
        ref_nodes = format_references(
            foot_domain.reference_style, FootReferenceText, node['reftype'],
            references).render(domain.backend)
        return ref_nodes, []
