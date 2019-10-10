"""
    .. autoclass:: BibliographyDirective

        .. automethod:: run
"""

import os.path  # normpath

from docutils.parsers.rst import Directive, directives

from ..bibtex.cache import process_bibfile
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

    required_arguments = 1
    optional_arguments = 0
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
        id_ = 'footbib-bibliography-%s-%s' % (
            env.docname, env.new_serialno('footbib'))
        bibcache = BibliographyCache(
            style=self.options.get(
                "style", env.app.config.footbib_default_style),
            encoding=self.options.get(
                'encoding',
                self.state.document.settings.input_encoding),
            bibfiles=[],
        )
        for bibfile in self.arguments[0].split():
            # convert to normalized absolute path to ensure that the same file
            # only occurs once in the cache
            bibfile = os.path.normpath(env.relfn2path(bibfile.strip())[1])
            process_bibfile(
                env.footbib_cache.bibfiles, bibfile, bibcache.encoding)
            env.note_dependency(bibfile)
            bibcache.bibfiles.append(bibfile)
        env.footbib_cache.bibliographies[env.docname][id_] = bibcache
        return [bibliography('', ids=[id_])]
