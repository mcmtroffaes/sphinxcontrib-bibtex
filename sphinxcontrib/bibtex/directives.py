"""
    New Doctree Directives
    ~~~~~~~~~~~~~~~~~~~~~~

    .. autoclass:: BibliographyDirective

        .. automethod:: run
        .. automethod:: process_bibfile
        .. automethod:: update_bibfile_cache
        .. automethod:: parse_bibfile

    .. autofunction:: process_start_option
"""

import ast  # parse(), used for filter
import os.path  # getmtime()

from docutils.parsers.rst import directives  # for Directive.option_spec
from sphinx.util.compat import Directive
from sphinx.util.console import bold, standout

from pybtex.database.input import bibtex
from pybtex.database import BibliographyData

from sphinxcontrib.bibtex.cache import BibliographyCache, BibfileCache
from sphinxcontrib.bibtex.nodes import bibliography

# register the latex codec
import latexcodec  # noqa


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
        'disable-curly-bracket-strip': directives.flag,
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
                env.app.warn(standout(":filter: overrides :all:"))
            if "notcited" in self.options:
                env.app.warn(standout(":filter: overrides :notcited:"))
            if "cited" in self.options:
                env.app.warn(standout(":filter: overrides :cited:"))
            try:
                filter_ = ast.parse(self.options["filter"])
            except SyntaxError:
                env.app.warn(
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
                'latex+' + self.state.document.settings.input_encoding),
            curly_bracket_strip=(
                'disable-curly-bracket-strip' not in self.options),
            labelprefix=self.options.get("labelprefix", ""),
            keyprefix=self.options.get("keyprefix", ""),
            labels={},
            bibfiles=[],
        )
        if (bibcache.list_ not in set(["bullet", "enumerated", "citation"])):
            env.app.warn(
                "unknown bibliography list type '{0}'.".format(bibcache.list_))
        for bibfile in self.arguments[0].split():
            # convert to normalized absolute path to ensure that the same file
            # only occurs once in the cache
            bibfile = os.path.normpath(env.relfn2path(bibfile.strip())[1])
            self.process_bibfile(bibfile, bibcache.encoding)
            env.note_dependency(bibfile)
            bibcache.bibfiles.append(bibfile)
        env.bibtex_cache.set_bibliography_cache(env.docname, id_, bibcache)
        return [bibliography('', ids=[id_])]

    def parse_bibfile(self, bibfile, encoding):
        """Parse *bibfile*, and return parsed data.

        :param bibfile: The bib file name.
        :type bibfile: ``str``
        :return: The parsed bibliography data.
        :rtype: :class:`pybtex.database.BibliographyData`
        """
        app = self.state.document.settings.env.app
        parser = bibtex.Parser(encoding)
        app.info(
            bold("parsing bibtex file {0}... ".format(bibfile)), nonl=True)
        parser.parse_file(bibfile)
        app.info("parsed {0} entries"
                 .format(len(parser.data.entries)))
        return parser.data

    def update_bibfile_cache(self, bibfile, mtime, encoding):
        """Parse *bibfile* (see :meth:`parse_bibfile`), and store the
        parsed data, along with modification time *mtime*, in the
        bibtex cache.

        :param bibfile: The bib file name.
        :type bibfile: ``str``
        :param mtime: The bib file's modification time.
        :type mtime: ``float``
        :return: The parsed bibliography data.
        :rtype: :class:`pybtex.database.BibliographyData`
        """
        data = self.parse_bibfile(bibfile, encoding)
        env = self.state.document.settings.env
        env.bibtex_cache.bibfiles[bibfile] = BibfileCache(
            mtime=mtime,
            data=data)
        return data

    def process_bibfile(self, bibfile, encoding):
        """Check if ``env.bibtex_cache.bibfiles[bibfile]`` is still
        up to date. If not, parse the *bibfile* (see
        :meth:`update_bibfile_cache`), and store parsed data in the
        bibtex cache.

        :param bibfile: The bib file name.
        :type bibfile: ``str``
        :return: The parsed bibliography data.
        :rtype: :class:`pybtex.database.BibliographyData`
        """
        env = self.state.document.settings.env
        cache = env.bibtex_cache.bibfiles
        # get modification time of bibfile
        try:
            mtime = os.path.getmtime(bibfile)
        except OSError:
            env.app.warn(
                standout("could not open bibtex file {0}.".format(bibfile)))
            cache[bibfile] = BibfileCache(  # dummy cache
                mtime=-float("inf"), data=BibliographyData())
            return cache[bibfile].data
        # get cache and check if it is still up to date
        # if it is not up to date, parse the bibtex file
        # and store it in the cache
        env.app.info(
            bold("checking for {0} in bibtex cache... ".format(bibfile)),
            nonl=True)
        try:
            bibfile_cache = cache[bibfile]
        except KeyError:
            env.app.info("not found")
            self.update_bibfile_cache(bibfile, mtime, encoding)
        else:
            if mtime != bibfile_cache.mtime:
                env.app.info("out of date")
                self.update_bibfile_cache(bibfile, mtime, encoding)
            else:
                env.app.info('up to date')
        return cache[bibfile].data
