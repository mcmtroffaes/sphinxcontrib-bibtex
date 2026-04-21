"""
.. autoclass:: FootBibliographyDirective

    .. automethod:: run
"""

from collections.abc import Sequence
from typing import TYPE_CHECKING, cast

import docutils.nodes
from sphinx.util.docutils import SphinxDirective

from .bibfile import _make_ids

if TYPE_CHECKING:
    from sphinx.environment import BuildEnvironment

    from .domain import BibtexDomain


class FootBibliographyDirective(SphinxDirective):
    """Class for processing the :rst:dir:`footbibliography` directive."""

    required_arguments = 0
    optional_arguments = 0
    has_content = False

    def run(self) -> Sequence[docutils.nodes.Node]:
        """Set file dependencies, and insert the footnotes that were created
        earlier by :meth:`.foot_roles.FootCiteRole.run`.
        """
        env = cast("BuildEnvironment", self.state.document.settings.env)
        foot_old_refs = env.temp_data.setdefault("bibtex_foot_old_refs", set())
        foot_new_refs = env.temp_data.setdefault("bibtex_foot_new_refs", set())
        footbibliography_count = env.temp_data["bibtex_footbibliography_count"] = (
            cast(int, env.temp_data.get("bibtex_footbibliography_count", 0)) + 1
        )
        if not foot_new_refs:
            return []
        else:
            # header
            header = getattr(env.config, "bibtex_footbibliography_header")
            header_nodes: list[docutils.nodes.Node] = (
                self.parse_text_to_nodes(header) if header else []
            )
            foot_old_refs |= foot_new_refs
            foot_new_refs.clear()
            # bibliography stored in env.temp_data["bibtex_foot_bibliography"]
            foot_bibliography, env.temp_data["bibtex_foot_bibliography"] = (
                env.temp_data["bibtex_foot_bibliography"],
                docutils.nodes.container(),
            )
            domain = cast("BibtexDomain", env.get_domain("cite"))
            for bibfile in domain.bibdata.bibfiles:
                env.note_dependency(bibfile)
            foot_bibliography["ids"] += _make_ids(
                docname=env.docname,
                lineno=self.lineno,
                ids=set(self.state.document.ids.keys()),
                raw_id=env.config.bibtex_footbibliography_id.format(
                    footbibliography_count=footbibliography_count
                ),
            )
            self.state.document.note_explicit_target(
                foot_bibliography, foot_bibliography
            )
            return header_nodes + [foot_bibliography]
