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

    """

    def __init__(self):
        self.bibfiles = {}
        self.bibliographies = {}

    def purge(self, docname):
        """Remove  all information related to *docname*.

        :param docname: The document name.
        :type docname: :class:`str`
        """
        ids = [id_ for id_, info in self.bibliographies.iteritems()
               if info.docname == docname]
        for id_ in ids:
            del self.bibliographies[id_]

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

    """

    def __init__(self, docname=None, bibfiles=None,
                 cite="cited", style=None, encoding=None,
                 curly_bracket_strip=True):
        self.docname = docname
        self.bibfiles = bibfiles if bibfiles is not None else []
        self.cite = cite
        self.style = style
        self.encoding = encoding
        self.curly_bracket_strip = curly_bracket_strip

