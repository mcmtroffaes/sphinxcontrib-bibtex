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
        # create id and cache for this node
        # this id will be stored with the node
        # and is used to look up additional data in env.footbib_cache
        # (implementation note: new_serialno only guarantees unique
        # ids within a single document, but we need the id to be
        # unique across all documents, so we also include the docname
        # in the id)
        bibcache = BibliographyCache(
            style=self.options.get(
                "style", env.app.config.footbib_default_style),
        )
        cache = env.footbib_cache
        for bibfile in cache.bibfiles:
            env.note_dependency(bibfile)
        id_ = cache.current_id[env.docname]
        cache.bibliographies[env.docname][id_] = bibcache
        cache.new_current_id(env)
        return [bibliography('', ids=[id_])]
