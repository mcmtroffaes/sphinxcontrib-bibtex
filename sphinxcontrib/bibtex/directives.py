"""
    New Doctree Directives
    ~~~~~~~~~~~~~~~~~~~~~~

    .. autoclass:: BibliographyDirective

        .. automethod:: run

    .. autofunction:: process_start_option
"""

import ast  # parse(), used for filter
import os.path  # getmtime()
import sphinx.util

from docutils.parsers.rst import Directive, directives
from sphinx.util.console import standout

from sphinxcontrib.bibtex.cache import BibliographyCache, process_bibfile
from sphinxcontrib.bibtex.nodes import bibliography


logger = sphinx.util.logging.getLogger(__name__)


def process_start_option(value):
    """Process and validate the start option value
    of a :rst:dir:`bibliography` directive.
    If *value* is ``continue`` then this function returns -1,
    otherwise *value* is converted into a positive integer.
    """
    if value == "continue":
        return -1
    else:
        return directives.positive_int(value)


class BibliographyDirective(Directive):

    """Class for processing the :rst:dir:`bibliography` directive.

    Parses the bibliography files, and produces a
    :class:`~sphinxcontrib.bibtex.nodes.bibliography` node.

    .. seealso::

       Further processing of the resulting
       :class:`~sphinxcontrib.bibtex.nodes.bibliography` node is done
       by
       :class:`~sphinxcontrib.bibtex.transforms.BibliographyTransform`.
    """

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = False
    option_spec = {
        'cited': directives.flag,
        'notcited': directives.flag,
        'all': directives.flag,
        'filter': directives.unchanged,
        'style': directives.unchanged,
        'list': directives.unchanged,
        'enumtype': directives.unchanged,
        'start': process_start_option,
        'encoding': directives.encoding,
        'labelprefix': directives.unchanged,
        'keyprefix': directives.unchanged,
    }

    def run(self):
        """Process .bib files, set file dependencies, and create a
        node that is to be transformed to the entries of the
        bibliography.
        """
        env = self.state.document.settings.env
        # create id and cache for this node
        # this id will be stored with the node
        # and is used to look up additional data in env.bibtex_cache
        # (implementation note: new_serialno only guarantees unique
        # ids within a single document, but we need the id to be
        # unique across all documents, so we also include the docname
        # in the id)
        id_ = 'bibtex-bibliography-%s-%s' % (
            env.docname, env.new_serialno('bibtex'))
        if "filter" in self.options:
            if "all" in self.options:
                logger.warning(standout(":filter: overrides :all:"))
            if "notcited" in self.options:
                logger.warning(standout(":filter: overrides :notcited:"))
            if "cited" in self.options:
                logger.warning(standout(":filter: overrides :cited:"))
            try:
                filter_ = ast.parse(self.options["filter"])
            except SyntaxError:
                logger.warning(
                    standout("syntax error in :filter: expression") +
                    " (" + self.options["filter"] + "); "
                    "the option will be ignored"
                )
                filter_ = ast.parse("cited")
        elif "all" in self.options:
            filter_ = ast.parse("True")
        elif "notcited" in self.options:
            filter_ = ast.parse("not cited")
        else:
            # the default filter: include only cited entries
            filter_ = ast.parse("cited")
        bibcache = BibliographyCache(
            list_=self.options.get("list", "citation"),
            enumtype=self.options.get("enumtype", "arabic"),
            start=self.options.get("start", 1),
            style=self.options.get(
                "style", env.app.config.bibtex_default_style),
            filter_=filter_,
            encoding=self.options.get(
                'encoding',
                self.state.document.settings.input_encoding),
            labelprefix=self.options.get("labelprefix", ""),
            keyprefix=self.options.get("keyprefix", ""),
            labels={},
            bibfiles=[],
        )
        if (bibcache.list_ not in set(["bullet", "enumerated", "citation"])):
            logger.warning(
                "unknown bibliography list type '{0}'.".format(bibcache.list_))
        for bibfile in self.arguments[0].split():
            # convert to normalized absolute path to ensure that the same file
            # only occurs once in the cache
            bibfile = os.path.normpath(env.relfn2path(bibfile.strip())[1])
            process_bibfile(
                env.bibtex_cache.bibfiles, bibfile, bibcache.encoding)
            env.note_dependency(bibfile)
            bibcache.bibfiles.append(bibfile)
        env.bibtex_cache.set_bibliography_cache(env.docname, id_, bibcache)
        return [bibliography('', ids=[id_])]
