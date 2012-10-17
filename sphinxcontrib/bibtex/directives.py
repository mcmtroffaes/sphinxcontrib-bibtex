"""
    New Doctree Directives
    ~~~~~~~~~~~~~~~~~~~~~~

    .. autoclass:: BibliographyDirective

        .. automethod:: run
        .. automethod:: process_bibfile
        .. automethod:: update_bibfile_cache
        .. automethod:: parse_bibfile
"""

import os.path # getmtime()

import copy # deepcopy
import docutils.nodes
from docutils.parsers.rst import directives # for Directive.option_spec
from sphinx.util.compat import Directive
from sphinx.util.console import bold, standout

from pybtex.database.input import bibtex

from sphinxcontrib.bibtex.cache import BibliographyCache, BibfileCache
import sphinxcontrib.bibtex.latex_codec # registers the latex codec
from sphinxcontrib.bibtex.nodes import bibliography

def process_start_option(value):
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
        'style': directives.unchanged,
        'list': directives.unchanged,
        'enumtype': directives.unchanged,
        'start': process_start_option,
        'encoding': directives.encoding,
        'disable-curly-bracket-strip': directives.flag,
        'labelprefix': directives.unchanged,
    }

    def run(self):
        """Process .bib files, set file dependencies, and create a
        node that is to be transformed to the entries of the
        bibliography.
        """
        env = self.state.document.settings.env
        cache = env.bibtex_cache.bibliographies
        # create id and cache for this node
        # this id will be stored with the node
        # and is used to look up additional data in env.bibtex_cache
        # (implementation note: new_serialno only guarantees unique
        # ids within a single document, but we need the id to be
        # unique across all documents, so we also include the docname
        # in the id)
        id_ = 'bibtex-bibliography-%s-%s' % (
            env.docname, env.new_serialno('bibtex'))
        info = BibliographyCache(
            docname=env.docname,
            cite=(
                "all"
                if "all" in self.options else (
                    "notcited"
                    if "notcited" in self.options else (
                        "cited"))),
            list_=self.options.get("list", "citation"),
            enumtype=self.options.get("enumtype", "arabic"),
            start=self.options.get("start", 1),
            style=self.options.get("style", "plain"),
            encoding=self.options.get(
                'encoding',
                'latex+' + self.state.document.settings.input_encoding),
            curly_bracket_strip=(
                'disable-curly-bracket-strip' not in self.options),
            labelprefix=self.options.get("labelprefix", ""),
            )
        if (info.list_ not in set(["bullet", "enumerated", "citation"])):
            env.app.warn(
                "unknown bibliography list type '{0}'.".format(info.list_))
        for bibfile in self.arguments[0].split():
            # convert to normalized absolute path to ensure that the same file
            # only occurs once in the cache
            bibfile = os.path.normpath(env.relfn2path(bibfile.strip())[1])
            self.process_bibfile(bibfile, info.encoding)
            env.note_dependency(bibfile)
            info.bibfiles.append(bibfile)
        cache[id_] = info
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
            cache[bibfile] = BibfileCache() # dummy cache
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
