"""
    .. autoclass:: FootBibliographyDirective

        .. automethod:: run
"""

from typing import cast

from docutils.parsers.rst import Directive
from sphinx.environment import BuildEnvironment

from .domain import BibtexDomain
from .foot_nodes import footbibliography


def new_foot_bibliography_id(env: BuildEnvironment) -> None:
    """Generate a new footbibliography id for the given build environment."""
    env.temp_data["bibtex_foot_bibliography_id"] = \
        'bibtex-footbibliography-%s-%s' % (
            env.docname, env.new_serialno('bibtex'))


class FootBibliographyDirective(Directive):

    """Class for processing the :rst:dir:`footbibliography` directive.

    Produces a :class:`~sphinxcontrib.bibtex.foot_nodes.footbibliography` node.

    .. seealso::

       Further processing of the resulting
       :class:`~sphinxcontrib.bibtex.foot_nodes.footbibliography` node is done
       by
       :class:`~sphinxcontrib.bibtex.foot_transforms.FootBibliographyTransform`.
    """

    required_arguments = 0
    optional_arguments = 0
    has_content = False

    def run(self):
        """Set file dependencies, update footbib id, and create a node
        that is to be transformed to the entries of the bibliography.
        """
        env = self.state.document.settings.env
        domain = cast(BibtexDomain, env.get_domain('cite'))
        for bibfile in domain.bibfiles:
            env.note_dependency(bibfile)
        id_ = env.temp_data["bibtex_foot_bibliography_id"]
        new_foot_bibliography_id(env)
        return [footbibliography('', ids=[id_])]
