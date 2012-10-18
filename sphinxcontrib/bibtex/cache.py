# -*- coding: utf-8 -*-
"""
    Cached Information
    ~~~~~~~~~~~~~~~~~~

    Classes and methods to maintain any information that is stored
    outside the doctree.

    .. autoclass:: Cache
        :members:

    .. autoclass:: BibfileCache
        :members:

    .. autoclass:: BibliographyCache
        :members:
"""

import collections
import pybtex.database

class Cache:
    """Global bibtex extension information cache. Stored in
    ``app.env.bibtex_cache``, so must be picklable.

    .. attribute:: bibfiles

        A :class:`dict` mapping .bib file names (relative to the top
        source folder) to :class:`BibfileCache` instances.

    .. attribute:: bibliographies

        Each bibliography directive is assigned an id of the form
        bibtex-bibliography-xxx. This :class:`dict` maps each such id
        to information about the bibliography directive,
        :class:`BibliographyCache`. We need to store this extra
        information separately because it cannot be stored in the
        :class:`~sphinxcontrib.bibtex.nodes.bibliography` nodes
        themselves.

    .. attribute:: _cited

        A :class:`dict` mapping each docname to a :class:`set` of
        citation keys.

    .. attribute:: _enum_count

        A :class:`dict` mapping each docname to an :class:`int`
        representing the current bibliography enumeration counter.

    """

    def __init__(self):
        self.bibfiles = {}
        self.bibliographies = {}
        self._cited = collections.defaultdict(set)
        self._enum_count = {}

    def purge(self, docname):
        """Remove  all information related to *docname*.

        :param docname: The document name.
        :type docname: :class:`str`
        """
        ids = [id_ for id_, info in self.bibliographies.iteritems()
               if info.docname == docname]
        for id_ in ids:
            del self.bibliographies[id_]
        self._cited.pop(docname, None)
        self._enum_count.pop(docname, None)

    def inc_enum_count(self, docname):
        if docname in self._enum_count:
            self._enum_count[docname] += 1
        else:
            self._enum_count[docname] = 2

    def set_enum_count(self, docname, value):
        self._enum_count[docname] = value

    def get_enum_count(self, docname):
        if docname in self._enum_count:
            return self._enum_count[docname]
        else:
            return 1

    def add_cited(self, key, docname):
        """Add the given *key* to the set of cited keys for
        *docname*.

        :param key: The citation key.
        :type key: :class:`str`
        :param docname: The document name.
        :type docname: :class:`str`
        """
        self._cited[docname].add(key)

    def is_cited(self, key):
        """Return whether the given key is cited in any document.

        :param key: The citation key.
        :type key: :class:`str`
        """
        for docname, keys in self._cited.iteritems():
            if key in keys:
                return True
        return False

    def get_label_from_key(self, key):
        """Return label for the given key."""
        for info in self.bibliographies.itervalues():
            if key in info.labels:
                return info.labels[key]
        else:
            raise KeyError("%s not found" % key)

class BibfileCache:
    """Contains information about a parsed .bib file.

    .. attribute:: mtime

        A :class:`float` representing the modification time of the .bib
        file when it was last parsed.

    .. attribute:: data

        A :class:`pybtex.database.BibliographyData` containing the
        parsed .bib file.

    """

    def __init__(self, mtime=None, data=None):
        self.mtime = mtime if mtime is not None else -float("inf")
        self.data = (data if data is not None
                     else pybtex.database.BibliographyData())

class BibliographyCache:
    """Contains information about a bibliography directive.

    .. attribute:: docname

        A :class:`str` containing the name of the document in which
        the directive occurs. We need this information during the
        Sphinx event *env-purge-doc*.

    .. attribute:: bibfiles

        A :class:`list` of :class:`str`\ s containing the .bib file
        names (relative to the top source folder) that contain the
        references.

    .. attribute:: cite

        A :class:`str`. Should be one of:

            ``"cited"``
                Only generate cited references.

            ``"notcited"``
                Only generated non-cited references.

            ``"all"``
                Generate all references from the .bib files.

    .. attribute:: style

        The bibtex style.

    .. attribute:: list_

        The list type.

    .. attribute:: enumtype

        The sequence type (only used for enumerated lists).

    .. attribute:: start

        The first ordinal of the sequence (only used for enumerated lists).

    .. attribute:: labels

        Maps citation keys to their final labels.

    .. attribute:: labelprefix

        This bibliography's string prefix for pybtex generated labels.
    """

    def __init__(self, docname=None, bibfiles=None,
                 cite="cited", style=None,
                 list_="citation", enumtype="arabic", start=1,
                 labels=None,
                 encoding=None,
                 curly_bracket_strip=True,
                 labelprefix="",
                 ):
        self.docname = docname
        self.bibfiles = bibfiles if bibfiles is not None else []
        self.cite = cite
        self.style = style
        self.list_ = list_
        self.enumtype = enumtype
        self.start = start
        self.encoding = encoding
        self.curly_bracket_strip = curly_bracket_strip
        self.labels = labels if labels is not None else {}
        self.labelprefix = labelprefix
