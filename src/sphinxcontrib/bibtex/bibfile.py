"""
    Classes and methods to work with bib files.

    .. autoclass:: BibFile
        :members:

    .. autofunction:: normpath_filename

    .. autofunction:: parse_bibfile

    .. autofunction:: process_bibfile

    .. autofunction:: get_bibliography_entry
"""
import math
import os.path
from typing import TYPE_CHECKING, Dict, Optional, NamedTuple, List, Set

from pybtex.database.input.bibtex import Parser
from sphinx.util.logging import getLogger

if TYPE_CHECKING:
    from pybtex.database import BibliographyData, Entry
    from sphinx.environment import BuildEnvironment


logger = getLogger(__name__)


class BibFile(NamedTuple):
    """Contains information about a parsed bib file."""
    mtime: float    #: Modification time of file when last parsed.
    keys: Set[str]  #: Set of keys for this bib file.


class BibData(NamedTuple):
    """Contains information about a collection of bib files."""
    encoding: str
    bibfiles: Dict[str, BibFile]
    data: "BibliographyData"


def normpath_filename(env: "BuildEnvironment", filename: str) -> str:
    """Return normalised path to *filename* for the given environment *env*."""
    return os.path.normpath(env.relfn2path(filename.strip())[1])


def get_mtime(bibfilename: str) -> float:
    try:
        return os.path.getmtime(bibfilename)
    except OSError:
        return -math.inf


def parse_bibfiles(bibfilenames: List[str], encoding: str) -> BibData:
    """Parse *bibfilenames* with given *encoding*, and return parsed data."""
    parser = Parser(encoding)
    bibfiles = {}
    keys: Set[str] = set()
    for filename in bibfilenames:
        logger.info("parsing bibtex file {0}... ".format(filename), nonl=True)
        if not os.path.isfile(filename):
            logger.warning(
                "could not open bibtex file {0}.".format(filename),
                type="bibtex", subtype="bibfile_error")
            new_keys = set()
        else:
            parser.parse_file(filename)
            keys, old_keys = set(parser.data.entries.keys()), keys
            assert old_keys <= keys
            new_keys = keys - old_keys
            logger.info("parsed {0} entries".format(len(new_keys)))
        bibfiles[filename] = BibFile(mtime=get_mtime(filename), keys=new_keys)
    return BibData(encoding=encoding, bibfiles=bibfiles, data=parser.data)


def is_bibdata_outdated(bibdata: BibData,
                        bibfilenames: List[str], encoding: str) -> bool:
    if bibdata.encoding != encoding:
        return True
    if list(bibdata.bibfiles) != bibfilenames:
        return True
    if any(bibfile.mtime != get_mtime(filename)
           for filename, bibfile in bibdata.bibfiles.items()):
        return True
    return False


def process_bibfile(bibdata: BibData,
                    bibfilenames: List[str], encoding: str) -> BibData:
    """Parse *bibfilenames* and store parsed data in *bibdata*."""
    logger.info("checking bibtex cache... ", nonl=True)
    if is_bibdata_outdated(bibdata, bibfilenames, encoding):
        logger.info("out of date")
        return parse_bibfiles(bibfilenames, encoding)
    else:
        logger.info("up to date")
        return bibdata


def get_bibliography_entry(bibdata: BibData, key: str) -> Optional["Entry"]:
    """Return bibliography entry from *bibfiles* for the given *key*."""
    try:
        return bibdata.data.entries[key]
    except KeyError:
        return None
