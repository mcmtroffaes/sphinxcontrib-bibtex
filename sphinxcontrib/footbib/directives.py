"""
    .. autoclass:: BibliographyDirective

        .. automethod:: run
"""

from docutils.parsers.rst import Directive, directives

from ..bibtex.cache import normpath_bibfile, process_bibfile
from .cache import BibliographyCache, new_id
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
    optional_arguments = 32
    final_argument_whitespace = True
    has_content = False
    option_spec = {
        'style': directives.unchanged,
        'encoding': directives.encoding,
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
            encoding=self.options.get(
                "encoding", env.app.config.footbib_default_encoding),
            # convert to normalized absolute path to ensure that the same file
            # only occurs once in the cache
            bibfiles=[
                normpath_bibfile(env, bibfile) for bibfile in (
                    self.arguments or env.app.config.footbib_default_bibfiles)
                ],
        )
        cache = env.footbib_cache
        for bibfile in bibcache.bibfiles:
            process_bibfile(
                cache.bibfiles, bibfile, bibcache.encoding)
            env.note_dependency(bibfile)
        id_ = cache.current_id[env.docname]
        cache.bibliographies[env.docname][id_] = bibcache
        cache.current_id[env.docname] = new_id(env)
        return [bibliography('', ids=[id_])]
