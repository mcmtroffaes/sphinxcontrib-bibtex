# -*- coding: utf-8 -*-
"""
    Classes and methods to work with bib files.

    .. autoclass:: BibfileCache
        :members:

    .. autofunction:: normpath_filename

    .. autofunction:: parse_bibfile

    .. autofunction:: process_bibfile

    .. autofunction:: get_bibliography_entry
"""

import copy
import os.path
from typing import NamedTuple, Dict

from pybtex.database.input import bibtex
from pybtex.database import BibliographyData, Entry
import sphinx.util
from sphinx.environment import BuildEnvironment
from sphinx.util.console import bold, standout


logger = sphinx.util.logging.getLogger(__name__)


#: Contains information about a parsed bib file.
class BibfileCache(NamedTuple):
    #: modification time of the bib file when last parsed
    mtime: float
    #: parsed bib file
    data: BibliographyData


def normpath_filename(env: BuildEnvironment, filename: str) -> str:
    """Return normalised path to *filename* for the given environment *env*."""
    return os.path.normpath(env.relfn2path(filename.strip())[1])


def parse_bibfile(bibfile: str, encoding: str) -> BibliographyData:
    """Parse *bibfile* with given *encoding*, and return parsed data."""
    parser = bibtex.Parser(encoding)
    logger.info(
        bold("parsing bibtex file {0}... ".format(bibfile)), nonl=True)
    parser.parse_file(bibfile)
    logger.info("parsed {0} entries"
                .format(len(parser.data.entries)))
    return parser.data


def process_bibfile(cache: Dict[str, BibfileCache],
                    bibfile: str, encoding: str) -> BibliographyData:
    """Check if ``cache[bibfile]`` is still up to date. If not, parse
    *bibfile*, store parsed data in *cache*, and return the data.
    """
    # get modification time of bibfile
    try:
        mtime = os.path.getmtime(bibfile)
    except OSError:
        logger.warning(
            standout("could not open bibtex file {0}.".format(bibfile)))
        cache[bibfile] = BibfileCache(  # dummy cache
            mtime=-float("inf"), data=BibliographyData())
        return cache[bibfile].data
    # get cache and check if it is still up to date
    # if it is not up to date, parse the bibtex file
    # and store it in the cache
    logger.info(
        bold("checking for {0} in bibtex cache... ".format(bibfile)),
        nonl=True)
    try:
        bibfile_cache = cache[bibfile]
    except KeyError:
        logger.info("not found")
        cache[bibfile] = BibfileCache(
            mtime=mtime, data=parse_bibfile(bibfile, encoding))
    else:
        if mtime != bibfile_cache.mtime:
            logger.info("out of date")
            cache[bibfile] = BibfileCache(
                mtime=mtime, data=parse_bibfile(bibfile, encoding))
        else:
            logger.info('up to date')
    return cache[bibfile].data


def get_bibliography_entry(cache: Dict[str, BibfileCache], key: str) -> Entry:
    """Return bibliography entry from *cache* for the given *key*."""
    for bibfile_cache in cache.values():
        data = bibfile_cache.data
        try:
            entry = data.entries[key]
        except KeyError:
            pass
        else:
            # entries are modified in an unpickable way
            # when formatting, so fetch a deep copy
            # and return this copy
            # we do not deep copy entry.collection because that
            # consumes enormous amounts of memory
            entry.collection = None
            entry2 = copy.deepcopy(entry)
            entry2.key = entry.key
            entry2.collection = data
            entry.collection = data
            return entry
    else:
        logger.warning("could not find bibtex key {0}.".format(key))
