# -*- coding: utf-8 -*-
"""
    Classes and methods to maintain any footbib information that is stored
    outside the doctree.

    .. autoclass:: Cache
        :members:
"""

import collections
from oset import oset


def _defaultdict_oset():
    return collections.defaultdict(oset)


class Cache:

    """Global footbib extension information cache. Stored in
    ``app.env.footbib_cache``, so must be picklable.
    """

    cited = None
    """A :class:`dict` mapping each docname to another :class:`dict`
    which maps each id to a :class:`set` of footnote keys.
    """

    current_id = None
    """A :class:`dict` mapping each docname to the currently active id."""

    def __init__(self):
        self.cited = collections.defaultdict(_defaultdict_oset)
        self.current_id = {}

    def purge(self, docname):
        """Remove all information related to *docname*.

        :param docname: The document name.
        :type docname: :class:`str`
        """
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
            self.cited[docname] = other.cited[docname]
            self.current_id[docname] = other.current_id[docname]

    def new_current_id(self, env):
        """Generate a new id for the given build environment."""
        self.current_id[env.docname] = 'bibtex-footbibliography-%s-%s' % (
            env.docname, env.new_serialno('bibtex'))
