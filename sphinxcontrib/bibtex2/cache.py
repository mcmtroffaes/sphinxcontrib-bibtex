# -*- coding: utf-8 -*-
"""
    Classes and methods to maintain any footbib information that is stored
    outside the doctree.

    .. autoclass:: Cache
        :members:
"""

import collections
import copy
from oset import oset
import sphinx.util


logger = sphinx.util.logging.getLogger(__name__)


def _defaultdict_oset():
    return collections.defaultdict(oset)


class Cache:

    """Global footbib extension information cache. Stored in
    ``app.env.footbib_cache``, so must be picklable.
    """

    bibliographies = None
    """Each bibliography directive is assigned an id of the form
    bibtex-footbibliography-xxx. This :class:`dict` maps each docname
    to another :class:`dict` which maps each id
    to information about the bibliography directive,
    :class:`BibliographyCache`. We need to store this extra
    information separately because it cannot be stored in the
    :class:`~sphinxcontrib.bibtex2.nodes.bibliography` nodes
    themselves.
    """

    cited = None
    """A :class:`dict` mapping each docname to another :class:`dict`
    which maps each id to a :class:`set` of footnote keys.
    """

    current_id = None
    """A :class:`dict` mapping each docname to the currently active
    bibtex-footbibliography-xxx id.
    """

    def __init__(self):
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
        for docname in docnames:
            self.bibliographies[docname] = other.bibliographies[docname]
            self.cited[docname] = other.cited[docname]
            self.current_id[docname] = other.current_id[docname]

    def new_current_id(self, env):
        """Generate a new footbib id for the given build environment."""
        self.current_id[env.docname] = 'bibtex-footbibliography-%s-%s' % (
            env.docname, env.new_serialno('bibtex'))

    def get_bibliography_entries(self, docname, id_, bibfiles):
        """Return filtered footnote bibliography entries, sorted by
        citation order.
        """
        # order entries according to which were cited first
        sorted_entries = []
        for key in self.cited[docname][id_]:
            for bibfile_cache in bibfiles.values():
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
                logger.warning("could not find bibtex key {0}.".format(key))
        return sorted_entries
