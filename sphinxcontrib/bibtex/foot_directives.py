"""
    .. autoclass:: FootBibliographyDirective

        .. automethod:: run
"""
from typing import cast

from docutils.parsers.rst import Directive

from .cache import BibtexDomain
from .foot_nodes import footbibliography


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
        domain = cast(BibtexDomain, env.get_domain('bibtex'))
        for bibfile in domain.bibfiles:
            env.note_dependency(bibfile)
        id_ = env.temp_data["bibtex_footbibliography_id"]
        domain.new_footbibliography_id()
        return [footbibliography('', ids=[id_])]
