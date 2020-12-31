"""
    Classes and methods to work with bib files.

    .. autoclass:: BibFile
        :members:

    .. autofunction:: normpath_filename

    .. autofunction:: parse_bibfile

    .. autofunction:: process_bibfile

    .. autofunction:: get_bibliography_entry
"""

import os.path
from typing import TYPE_CHECKING, Dict, Optional, NamedTuple

from pybtex.database.input.bibtex import Parser
from sphinx.util.logging import getLogger

if TYPE_CHECKING:
    from pybtex.database import BibliographyData, Entry
    from sphinx.environment import BuildEnvironment


logger = getLogger(__name__)


class BibFile(NamedTuple):
    """Contains information about a parsed bib file."""
    mtime: float              #: modification time of bib file when last parsed
    data: "BibliographyData"  #: parsed data from pybtex


def normpath_filename(env: "BuildEnvironment", filename: str) -> str:
    """Return normalised path to *filename* for the given environment *env*."""
    return os.path.normpath(env.relfn2path(filename.strip())[1])


def parse_bibfile(bibfilename: str, encoding: str) -> "BibliographyData":
    """Parse *bibfilename* with given *encoding*, and return parsed data."""
    parser = Parser(encoding)
    logger.info("parsing bibtex file {0}... ".format(bibfilename), nonl=True)
    parser.parse_file(bibfilename)
    logger.info("parsed {0} entries"
                .format(len(parser.data.entries)))
    return parser.data


def process_bibfile(bibfiles: Dict[str, BibFile],
                    bibfilename: str, encoding: str) -> None:
    """Check if *bibfiles* is still up to date. If not, parse
    *bibfilename* and store parsed data in *bibfiles*.
    """
    try:
        mtime = os.path.getmtime(bibfilename)
    except OSError:
        logger.warning(
            "could not open bibtex file {0}.".format(bibfilename))
        return
    # get cache and check if it is still up to date
    # if it is not up to date, parse the bibtex file
    # and store it in the cache
    logger.info("checking for {0} in bibtex cache... ".format(bibfilename),
                nonl=True)
    try:
        bibfile = bibfiles[bibfilename]
    except KeyError:
        logger.info("not found")
        bibfiles[bibfilename] = BibFile(
            mtime=mtime, data=parse_bibfile(bibfilename, encoding))
    else:
        if mtime != bibfile.mtime:
            logger.info("out of date")
            bibfiles[bibfilename] = BibFile(
                mtime=mtime, data=parse_bibfile(bibfilename, encoding))
        else:
            logger.info('up to date')


def get_bibliography_entry(
        bibfiles: Dict[str, BibFile], key: str) -> Optional["Entry"]:
    """Return bibliography entry from *bibfiles* for the given *key*."""
    for bibfile in bibfiles.values():
        try:
            return bibfile.data.entries[key]
        except KeyError:
            pass
    else:
        return None
