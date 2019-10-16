# -*- coding: utf-8 -*-
"""
    Classes and methods to maintain any footbib information that is stored
    outside the doctree.

    .. autoclass:: Cache
        :members:

    .. autoclass:: BibliographyCache
        :members:
"""

import collections
import copy
from oset import oset

import sphinx.util
from sphinx.util.console import standout


logger = sphinx.util.logging.getLogger(__name__)


def new_id(env):
    """Generate a new footbib id for the given build environment."""
    return 'footbib-bibliography-%s-%s' % (
        env.docname, env.new_serialno('footbib'))


def _defaultdict_oset():
    return collections.defaultdict(oset)


class Cache:

    """Global footbib extension information cache. Stored in
    ``app.env.footbib_cache``, so must be picklable.
    """

    bibfiles = None
    """A :class:`dict` mapping .bib file names to
    :class:`~sphinxcontrib.bibtex.BibfileCache` instances.
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
    """A :class:`dict` mapping each docname to another :class:`dict`
    which maps each id to a :class:`set` of footnote keys.
    """

    current_id = None
    """A :class:`dict` mapping each docname to the currently active
    footbib-bibliography-xxx id.
    """

    def __init__(self):
        self.bibfiles = {}
        self.bibliographies = collections.defaultdict(dict)
        self.cited = collections.defaultdict(_defaultdict_oset)
        self.current_id = collections.defaultdict(dict)

    def purge(self, docname):
        """Remove all information related to *docname*.

        :param docname: The document name.
        :type docname: :class:`str`
        """
        self.bibliographies.pop(docname, None)
        self.cited.pop(docname, None)
        self.current_id.pop(docname, None)

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
            self.current_id[docname] = other.current_id[docname]

    def get_bibliography_entries(self, docname, id_):
        """Return filtered footnote bibliography entries, sorted by
        citation order.
        """
        # order entries according to which were cited first
        sorted_entries = []
        bibcache = self.bibliographies[docname][id_]
        for key in self.cited[docname][id_]:
            for bibfile_cache in self.bibfiles.values():
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
                    sorted_entries.append(entry)
                    break
            else:
                logger.warning(
                    standout("could not find bibtex key {0}.".format(key)))
        return sorted_entries


class BibliographyCache(collections.namedtuple(
    'BibliographyCache',
    """style
""")):

    """Contains information about a footbibliography directive.

    .. attribute:: style

        The bibtex style.
    """
