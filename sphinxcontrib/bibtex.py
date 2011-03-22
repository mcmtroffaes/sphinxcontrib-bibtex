# -*- coding: utf-8 -*-
"""
    sphinxcontrib.bibtex
    ~~~~~~~~~~~~~~~~~~~~

    Allow bibtex references to be inserted into your documentation.

    :author: Matthias C. M. Troffaes <matthias.troffaes@gmail.com>
    :license: BSD, see LICENSE for details

    Inspired by ``bibstuff.sphinxext.bibref`` by Matthew Brett.

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
from sphinx.util.console import bold, standout

from pybtex.database.input import bibtex

def parse_bibfile(app, bibfile):
    """Parse *bibfile*, and return parsed data.

    :param app: The sphinx application.
    :type app: :class:`Sphinx`
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
    """Parse *bibfile*, and store the parsed data, along with
    modification time *mtime*, in the bibtex cache.

    :param app: The sphinx application.
    :type app: :class:`Sphinx`
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
    If not, parse the *bibfile*, and store parsed data in the bibtex
    cache.

    :param app: The sphinx application.
    :type app: :class:`Sphinx`
    :param bibfile: The bib file name.
    :type bibfile: ``str``
    """
    # get modification time of bibfile
    try:
        mtime = os.path.getmtime(bibfile)
    except OSError:
        app.warn(
            standout('could not open bibtex file {0}.'.format(bibfile)))
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
    """Check if ``app.env.bibtex_cache`` is still up-to-date."""
    if not hasattr(app.env, "bibtex_cache"):
        app.env.bibtex_cache = {}
    for bibfile in app.config.bibtex_bibfiles:
        process_bibfile(app, bibfile)

def setup(app):
    # register bibtex_bibfiles configuration value
    # it is a list of bibliography files
    app.add_config_value('bibtex_bibfiles', [], False)
    app.connect('builder-inited', init_bibtex_cache)
