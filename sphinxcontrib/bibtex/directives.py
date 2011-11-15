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

from docutils.parsers.rst import directives # for Directive.option_spec
from sphinx.util.compat import Directive
from sphinx.util.console import bold, standout

from pybtex.backends.doctree import Backend as output_backend
from pybtex.database.input import bibtex
from pybtex.plugin import find_plugin

from sphinxcontrib.bibtex.cache import BibliographyCache, BibfileCache
from sphinxcontrib.bibtex.nodes import bibliography
import sphinxcontrib.bibtex.latex_codec # registers the latex codec

class BibliographyDirective(Directive):
    """Class for processing the :rst:dir:`bibliography` directive."""

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = False
    option_spec = {
        'cited': directives.flag,
        'notcited': directives.flag,
        'all': directives.flag,
        'style': directives.unchanged,
    }

    def run(self):
        """Process .bib files, set file dependencies, and create a
        nodes for all entries of the bibliography.
        """
        env = self.state.document.settings.env
        cache = env.bibtex_cache.bibliographies
        # create id and cache for this node
        # this id will be stored with the node
        # and is used to look up additional data in env.bibtex_cache
        id_ = 'bibtex-bibliography-%s' % env.new_serialno('bibtex')
        info = BibliographyCache(
            docname=env.docname,
            cite=(
                "all"
                if "all" in self.options else (
                    "notcited"
                    if "notcited" in self.options else (
                        "cited"))),
            style=self.options.get("style", "unsrt"))
        cache[id_] = info
        # get all bibfiles
        for bibfile in self.arguments[0].split():
            # convert to relative path to ensure that the same file
            # only occurs once in the cache
            bibfile = env.relfn2path(bibfile.strip())[0]
            self.process_bibfile(bibfile)
            env.note_dependency(bibfile)
            info.bibfiles.append(bibfile)
        return [bibliography('', ids=[id_])]

    def parse_bibfile(self, bibfile):
        """Parse *bibfile*, and return parsed data.

        :param bibfile: The bib file name.
        :type bibfile: ``str``
        :return: The parsed bibliography data.
        :rtype: :class:`pybtex.database.BibliographyData`
        """
        app = self.state.document.settings.env.app
        parser = bibtex.Parser('latex') # TODO support inputenc
        app.info(
            bold("parsing bibtex file {0}... ".format(bibfile)), nonl=True)
        parser.parse_file(bibfile)
        app.info("parsed {0} entries"
                 .format(len(parser.data.entries)))
        return parser.data

    def update_bibfile_cache(self, bibfile, mtime):
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
        data = self.parse_bibfile(bibfile)
        env = self.state.document.settings.env
        env.bibtex_cache.bibfiles[bibfile] = BibfileCache(
            mtime=mtime,
            data=data)
        return data

    def process_bibfile(self, bibfile):
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
            self.update_bibfile_cache(bibfile, mtime)
        else:
            if mtime != bibfile_cache.mtime:
                env.app.info("out of date")
                self.update_bibfile_cache(bibfile, mtime)
            else:
                env.app.info('up to date')
        return cache[bibfile].data
