"""
    .. autoclass:: FootBibliographyDirective

        .. automethod:: run
"""

from typing import cast

from docutils.parsers.rst import Directive
from sphinx.environment import BuildEnvironment

from .domain import BibtexDomain


def new_foot_bibliography_id(env: BuildEnvironment) -> None:
    """Generate a new footbibliography id for the given build environment."""
    env.temp_data["bibtex_foot_bibliography_id"] = \
        'bibtex-footbibliography-%s-%s' % (
            env.docname, env.new_serialno('bibtex'))


class FootBibliographyDirective(Directive):

    """Class for processing the :rst:dir:`footbibliography` directive."""

    required_arguments = 0
    optional_arguments = 0
    has_content = False

    def run(self):
        """Set file dependencies, and insert the footnotes that were created
        earlier by :meth:`.foot_roles.FootCiteRole.result_nodes`.
        """
        env = cast(BuildEnvironment, self.state.document.settings.env)
        foot_old_refs = env.temp_data.setdefault("bibtex_foot_old_refs", set())
        foot_new_refs = env.temp_data.setdefault("bibtex_foot_new_refs", set())
        if not foot_new_refs:
            return []
        else:
            foot_old_refs |= foot_new_refs
            foot_new_refs.clear()
            # bibliography stored in env.temp_data["bibtex_foot_bibliography"]
            domain = cast(BibtexDomain, env.get_domain('cite'))
            foot_bibliography, env.temp_data["bibtex_foot_bibliography"] = (
                env.temp_data["bibtex_foot_bibliography"],
                domain.footbibliography_header.deepcopy())
            for bibfile in domain.bibfiles:
                env.note_dependency(bibfile)
            return [foot_bibliography]
