# -*- coding: utf-8 -*-
"""
    sphinxcontrib.bibtex
    ~~~~~~~~~~~~~~~~~~~~

    Allow bibtex references to be inserted into your documentation.

    :author: Matthias C. M. Troffaes <matthias.troffaes@gmail.com>
    :license: BSD, see LICENSE for details

    Inspired by ``bibstuff.sphinxext.bibref`` by Matthew Brett.

    Usage
    -----

    .. rst:role:: cite

       Create a citation to a bibliographic entry.

    .. rst:directive:: .. bibliography:: refs.bib [...]

       Create bibliography for all citations in the current document.

    Implementation notes
    --------------------

    ``app.env.bibtex_cache``
        Dictionary for caching parsed bibtex files. Each key is the
        name of a .bib file. The value is again a dictionary with keys
        ``"mtime"``, containing the modification time of the bibfile
        when it was last parsed, and ``"data"``, containing the parsed
        .bib file data, that is, a dictionary of citation keys to
        bibtex keys and their values.

    Extension API
    -------------
"""

import os.path

from docutils import nodes
from sphinx.util.compat import Directive
from sphinx.util.console import bold, standout
from sphinx.util.nodes import split_explicit_title
from sphinx.roles import XRefRole # for :cite:

from pybtex.database.input import bibtex

class bibliography(nodes.General, nodes.Element):
    """Node for representing a bibliography. Replaced by a list of
    citations on doctree-resolved.
    """
    pass

class BibliographyDirective(Directive):
    """Class for processing the bibliography directive."""

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = False

    def run(self):
        """Process .bib files, set file dependencies, and create a
        temporary node for the bibliography.
        """

        document = self.state.document
        env = self.state.document.settings.env
        for bibfile in self.arguments[0].split():
            # convert to relative path to ensure that the same file
            # only occurs once in the cache
            bibfile = env.relfn2path(bibfile.strip())[0]
            process_bibfile(env.app, bibfile)
            env.note_dependency(bibfile)
        ### for the time being we don't return anything
        return [] #[bibliography("")]

def parse_bibfile(app, bibfile):
    """Parse *bibfile*, and return parsed data.

    :param app: The :mod:`sphinx application <sphinx.application>`.
    :type app: :class:`sphinx.application.Sphinx`
    :param bibfile: The bib file name.
    :type bibfile: ``str``
    :return: The parsed bibliography data.
    :rtype: :class:`pybtex.database.BibliographyData`
    """
    parser = bibtex.Parser()
    app.info(bold("parsing bibtex file {0}... ".format(bibfile)), nonl=True)
    parser.parse_file(bibfile)
    app.info("parsed {0} entries"
             .format(len(parser.data.entries)))
    return parser.data

def update_bibfile_cache(app, bibfile, mtime):
    """Parse *bibfile* (see :func:`parse_bibfile`), and store the
    parsed data, along with modification time *mtime*, in the bibtex
    cache.

    :param app: The :mod:`sphinx application <sphinx.application>`.
    :type app: :class:`sphinx.application.Sphinx`
    :param bibfile: The bib file name.
    :type bibfile: ``str``
    :param mtime: The bib file's modification time.
    :type mtime: ``float``
    """
    app.env.bibtex_cache[bibfile] = {
        "mtime": mtime,
        "data": parse_bibfile(app, bibfile)}
    # TODO force the environment to be repickled
    # see sphinx/builders/__init__.py lines 234-239, self.env.topickle(...)

def process_bibfile(app, bibfile):
    """Check if ``app.env.bibtex_cache[bibfile]`` is still up-to-date.
    If not, parse the *bibfile* (see :func:`update_bibfile_cache`),
    and store parsed data in the bibtex cache.

    :param app: The :mod:`sphinx application <sphinx.application>`.
    :type app: :class:`sphinx.application.Sphinx`
    :param bibfile: The bib file name.
    :type bibfile: ``str``
    """
    # get modification time of bibfile
    try:
        mtime = os.path.getmtime(bibfile)
    except OSError:
        app.warn(
            standout("could not open bibtex file {0}.".format(bibfile)))
        return
    # get cache and check if it is still up to date
    # if it is not up to date, parse the bibtex file
    # and store it in the cache
    app.info(bold("checking for {0} in bibtex cache... ".format(bibfile)),
             nonl=True)
    try:
        bibfile_cache = app.env.bibtex_cache[bibfile]
    except KeyError:
        app.info("not found")
        update_bibfile_cache(app, bibfile, mtime)
    else:
        if mtime != bibfile_cache["mtime"]:
            app.info("out of date")
            update_bibfile_cache(app, bibfile, mtime)
        else:
            app.info('up to date')

def init_bibtex_cache(app):
    """Create ``app.env.bibtex_cache`` if it does not exist yet.

    :param app: The :mod:`sphinx application <sphinx.application>`.
    :type app: :class:`sphinx.application.Sphinx`
    """
    if not hasattr(app.env, "bibtex_cache"):
        app.env.bibtex_cache = {}

def setup(app):
    """Set up the bibtex extension.

    * register directives

      - :class:`BibliographyDirective` for :rst:dir:`bibliography`

    * register nodes

      - :class:`bibliography`

    * register roles

      - :rst:role:`cite`

    * connect events to functions

      **builder-inited**
          :func:`init_bibtex_cache`
    """
    app.add_directive("bibliography", BibliographyDirective)
    app.add_node(bibliography)
    app.add_role("cite", XRefRole())
    app.connect("builder-inited", init_bibtex_cache)
