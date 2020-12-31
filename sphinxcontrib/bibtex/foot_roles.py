"""
    .. autoclass:: FootCiteRole
        :show-inheritance:

        .. automethod:: result_nodes
"""

from typing import TYPE_CHECKING, cast, Tuple, List
from pybtex.plugin import find_plugin
from sphinx.roles import XRefRole
from sphinx.util.logging import getLogger

from .bibfile import get_bibliography_entry
from .transforms import node_text_transform, transform_url_command

if TYPE_CHECKING:
    import docutils.nodes
    from sphinx.environment import BuildEnvironment
    from .domain import BibtexDomain


logger = getLogger(__name__)


class FootCiteRole(XRefRole):
    """Class for processing the :rst:role:`footcite` role."""

    backend = find_plugin('pybtex.backends', 'docutils')()

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
        domain = cast("BibtexDomain", self.env.get_domain('cite'))
        keys = [key.strip() for key in self.target.split(',')]  # type: ignore
        try:
            foot_bibliography = env.temp_data["bibtex_foot_bibliography"]
        except KeyError:
            env.temp_data["bibtex_foot_bibliography"] = foot_bibliography = \
                domain.footbibliography_header.deepcopy()
        foot_old_refs = env.temp_data.setdefault("bibtex_foot_old_refs", set())
        foot_new_refs = env.temp_data.setdefault("bibtex_foot_new_refs", set())
        style = find_plugin(
            'pybtex.style.formatting',
            self.config.bibtex_default_style)()
        ref_nodes = []
        for key in keys:
            entry = get_bibliography_entry(domain.bibfiles, key)
            if entry is not None:
                ref_nodes.append(
                    self.backend.footnote_reference(entry, document))
                if key not in (foot_old_refs | foot_new_refs):
                    formatted_entry = style.format_entry(label='', entry=entry)
                    footnote = self.backend.footnote(formatted_entry, document)
                    node_text_transform(footnote, transform_url_command)
                    foot_bibliography += footnote
                    foot_new_refs.add(key)
            else:
                logger.warning('could not find bibtex key "%s"' % key,
                               location=(env.docname, self.lineno))
        return ref_nodes, []
