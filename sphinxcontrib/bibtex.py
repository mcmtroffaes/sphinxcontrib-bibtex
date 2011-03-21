# -*- coding: utf-8 -*-
"""
    sphinxcontrib.bibtex
    ~~~~~~~~~~~~~~~~~~~~

    Allow bibtex references to be inserted into your documentation.

    :author: Matthias C. M. Troffaes <matthias.troffaes@gmail.com>
    :license: BSD, see LICENSE for details

    Inspired by ``bibstuff.sphinxext.bibref`` by Matthew Brett.
"""

import os.path
from sphinx.util.console import bold, standout

from pybtex.database.input import bibtex

def parse_bibfiles(app, bibfiles):
    """Parse all *bibfiles*, and return parsed data."""
    parser = bibtex.Parser()
    app.info(bold("parsing bibtex files: "), nonl=True)
    for bibfile in bibfiles:
        app.info(bibfile + "... ", nonl=True)
        parser.parse_file(bibfile)
    app.info("parsed {0} entries"
             .format(len(parser.data.entries)))
    return parser.data

def update_bibtex_cache(app, files, mtimes):
    """Update the bibtex cache ``app.env.bibtex_cache``."""
    app.env.bibtex_cache = {
        "data": parse_bibfiles(app, files),
        "files": files,
        "mtimes": mtimes}
    # TODO force the environment to be repickled
    # see sphinx/builders/__init__.py lines 234-239, self.env.topickle(...)

def process_bibfiles(app):
    """Check if ``app.env.bibtex_cache`` is still up-to-date. If not,
    parse all bibfiles, and store parsed data in the environment as
    ``app.env.bibtex_cache``.
    """        

    # check bibfiles and their modification times
    # we store this list of files and their times in the bibtex_cache
    # this allows us to check whether things are still up to date or not
    files = []
    mtimes = []
    for bibfile in app.config.bibtex_bibfiles:
        try:
            mtimes.append(os.path.getmtime(bibfile))
        except OSError:
            app.warn(
                standout('could not open bibtex file {0}.'.format(bibfile)))
        else:
            files.append(bibfile)
    # check if bibtex_cache was loaded from pickled environment
    # and if it is still up to date
    app.info(bold("checking bibtex cache... "), nonl=True)
    if not hasattr(app.env, "bibtex_cache"):
        app.info("not found")
        update_bibtex_cache(app, files, mtimes)
    elif (app.env.bibtex_cache["files"] != files
          or app.env.bibtex_cache["mtimes"] != mtimes):
        app.info("out of date")
        update_bibtex_cache(app, files, mtimes)
    else:
        app.info('up to date')

def setup(app):
    # register bibtex_bibfiles configuration value
    # it is a list of bibliography files
    app.add_config_value('bibtex_bibfiles', [], False)
    app.connect('builder-inited', process_bibfiles)
