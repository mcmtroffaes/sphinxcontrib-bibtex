"""
    .. autoclass:: FootBibliographyDirective

        .. automethod:: run
"""

from docutils.parsers.rst import Directive

from .foot_nodes import bibliography


class FootBibliographyDirective(Directive):

    """Class for processing the :rst:dir:`footbibliography` directive.

    Produces a :class:`~sphinxcontrib.bibtex2.foot_nodes.bibliography` node.

    .. seealso::

       Further processing of the resulting
       :class:`~sphinxcontrib.bibtex2.foot_nodes.bibliography` node is done
       by
       :class:`~sphinxcontrib.bibtex2.foot_transforms.FootBibliographyTransform`.
    """

    required_arguments = 0
    optional_arguments = 0
    has_content = False

    def run(self):
        """Set file dependencies, update footbib id, and create a node
        that is to be transformed to the entries of the bibliography.
        """
        env = self.state.document.settings.env
        for bibfile in env.bibtex_cache.bibfiles:
            env.note_dependency(bibfile)
        id_ = env.bibtex_cache.foot_current_id[env.docname]
        env.bibtex_cache.new_foot_current_id(env)
        return [bibliography('', ids=[id_])]
