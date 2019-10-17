"""
    .. autoclass:: BibliographyDirective

        .. automethod:: run
"""

from docutils.parsers.rst import Directive, directives

from .cache import BibliographyCache
from .nodes import bibliography


class BibliographyDirective(Directive):

    """Class for processing the :rst:dir:`footbibliography` directive.

    Parses the bibliography files, and produces a
    :class:`~sphinxcontrib.footbib.nodes.bibliography` node.

    .. seealso::

       Further processing of the resulting
       :class:`~sphinxcontrib.footbib.nodes.bibliography` node is done
       by
       :class:`~sphinxcontrib.footbib.transforms.BibliographyTransform`.
    """

    required_arguments = 0
    optional_arguments = 0
    has_content = False
    option_spec = {
        'style': directives.unchanged,
    }

    def run(self):
        """Process .bib files, set file dependencies, and create a
        node that is to be transformed to the entries of the
        bibliography.
        """
        env = self.state.document.settings.env
        for bibfile in env.bibtex_bibfiles:
            env.note_dependency(bibfile)
        cache = env.footbib_cache
        id_ = cache.current_id[env.docname]
        cache.bibliographies[env.docname][id_] = BibliographyCache(
            style=self.options.get(
                "style", env.app.config.bibtex_style),
        )
        cache.new_current_id(env)
        return [bibliography('', ids=[id_])]
