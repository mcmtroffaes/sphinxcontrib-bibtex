# -*- coding: utf-8 -*-
"""
    Cached Information
    ~~~~~~~~~~~~~~~~~~

    Classes and methods to maintain any information that is stored
    outside the doctree.

    .. autoclass:: Cache
        :members:

    .. autoclass:: BibliographyCache
        :members:
"""

from collections import OrderedDict
import collections
import copy
import os.path  # getmtime()
from oset import oset
import re

import sphinx.util
from sphinx.util.console import bold, standout

from pybtex.database.input import bibtex
from pybtex.database import BibliographyData


logger = sphinx.util.logging.getLogger(__name__)


class Cache:

    """Global footbib extension information cache. Stored in
    ``app.env.footbib_cache``, so must be picklable.
    """

    bibfiles = None
    """A :class:`dict` mapping .bib file names (relative to the top
    source folder) to :class:`~sphinxcontrib.bibtex.BibfileCache`
    instances.
    """

    bibliographies = None
    """Each bibliography directive is assigned an id of the form
    footbib-bibliography-xxx. This :class:`dict` maps each docname
    to another :class:`dict` which maps each id
    to information about the bibliography directive,
    :class:`BibliographyCache`. We need to store this extra
    information separately because it cannot be stored in the
    :class:`~sphinxcontrib.footbib.nodes.bibliography` nodes
    themselves.
    """

    cited = None
    """A :class:`dict` mapping each docname to a :class:`set` of
    footnote keys.
    """

    def __init__(self):
        self.bibfiles = {}
        self.bibliographies = collections.defaultdict(dict)
        self.cited = collections.defaultdict(oset)

    def purge(self, docname):
        """Remove all information related to *docname*.

        :param docname: The document name.
        :type docname: :class:`str`
        """
        self.bibliographies.pop(docname, None)
        self.cited.pop(docname, None)

    def merge(self, docnames, other):
        """Merge information from *other* cache related to *docnames*.

        :param docnames: The document names.
        :type docnames: :class:`str`
        :param other: The other cache.
        :type other: :class:`Cache`
        """
        self.bibfiles.update(other.bibfiles)
        for docname in docnames:
            self.bibliographies[docname] = other.bibliographies[docname]
            self.cited[docname] = other.cited[docname]

    def get_bibliography_entries(self, docname, id_):
        """Return filtered footnote bibliography entries, sorted by
        citation order.
        """
        # order entries according to which were cited first
        sorted_entries = []
        bibcache = self.bibliographies[docname][id_]
        for key in self.cited[docname]:
            for bibfile in bibcache.bibfiles:
                data = self.bibfiles[bibfile].data
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
                    sorted_entries.append(entry)
                    break
            else:
                logger.warning(
                    standout("could not find bibtex key {0}.".format(key)))
        return sorted_entries


class BibliographyCache(collections.namedtuple(
    'BibliographyCache',
    """bibfiles style encoding
""")):

    """Contains information about a fnbibliography directive.

    .. attribute:: bibfiles

        A :class:`list` of :class:`str`\\ s containing the .bib file
        names (relative to the top source folder) that contain the
        references.

    .. attribute:: style

        The bibtex style.
    """
