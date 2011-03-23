# -*- coding: utf-8 -*-
"""
    sphinxcontrib.bibtex
    ~~~~~~~~~~~~~~~~~~~~

    Allow bibtex references to be inserted into your documentation.

    :author: Matthias C. M. Troffaes <matthias.troffaes@gmail.com>
    :license: BSD, see LICENSE for details

    Inspired by ``bibstuff.sphinxext.bibref`` by Matthew Brett.

    Usage
    =====

    .. rst:role:: cite

       Create a citation to a bibliographic entry.

    .. rst:directive:: .. bibliography:: refs.bib [...]

       Create bibliography for all citations in the current document.

    Extension API
    =============

"""

import os.path

from docutils import nodes
from docutils.parsers.rst import directives # for Directive.option_spec
from sphinx.util.compat import Directive
from sphinx.util.console import bold, standout
from sphinx.util.nodes import split_explicit_title
from sphinx.roles import XRefRole # for :cite:

from pybtex.database.input import bibtex

class BibtexInfo:
    """Stores bibliographic information. Used for
    ``app.env.bibtex_info``, so must be pickleable.

    .. attribute:: bibfiles

        A :class:`dict` mapping .bib file names (relative to the top
        source folder) to :class:`BibfileInfo` instances.

    .. attribute:: bibliographies

        Each bibliography directive is assigned an id of the form
        bibtex-bibliography-xxx. This :class:`dict` maps each such id
        to information about the bibliography directive,
        :class:`BibliographyInfo`. We need to store this extra
        information separately because it cannot be stored in the
        :class:`bibliography` nodes themselves.

    """

    def __init__(self):
        self.bibfiles = {}
        self.bibliographies = {}

class BibfileInfo:
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

class BibliographyInfo:
    """Contains information about a bibliography directive.

    .. attribute:: docname

        A :class:`str` containing the name of the document in
        which the directive occurs. We need this information
        during :ref:`sphinx:env-purge-doc`.

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
                 cite="cited", style=None):
        self.docname = docname
        self.bibfiles = bibfiles if bibfiles is not None else []
        self.cite = cite
        self.style = style

class bibliography(nodes.General, nodes.Element):
    """Node for representing a bibliography. Replaced by a list of
    citations or footnotes (depending on the authoryear option) on
    doctree-resolved.
    """
    pass

class cite(nodes.General, nodes.Element):
    """Node for representing a citation with the :rst:role:`cite`
    role.
    """
    pass

class BibliographyDirective(Directive):
    """Class for processing the bibliography directive."""

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = False
    option_spec = {
        'cited': directives.flag,
        'notcited': directives.flag,
        'all': directives.flag,
        'style': directives.unchanged,
    }

    def run(self):
        """Process .bib files, set file dependencies, and create a
        temporary node for the bibliography.
        """
        env = self.state.document.settings.env
        cache = env.bibtex_info.bibliographies
        # create id and cache for this node
        # this id will be stored with the node
        # and is used to look up additional data in env.bibtex_info
        id_ = 'bibtex-bibliography-%s' % env.new_serialno('index')
        info = BibliographyInfo(
            docname=env.docname,
            cite=(
                "all"
                if "all" in self.options else (
                    "notcited"
                    if "notcited" in self.options else (
                        "cited"))),
            style=self.options.get("style", "plain"))
        cache[id_] = info
        # get all bibfiles
        for bibfile in self.arguments[0].split():
            # convert to relative path to ensure that the same file
            # only occurs once in the cache
            bibfile = env.relfn2path(bibfile.strip())[0]
            process_bibfile(env.app, bibfile)
            env.note_dependency(bibfile)
            info.bibfiles.append(bibfile)
        return [bibliography('', ids=[id_])]

def parse_bibfile(app, bibfile):
    """Parse *bibfile*, and return parsed data.

    :param app: The :mod:`sphinx application <sphinx.application>`.
    :type app: :class:`sphinx.application.Sphinx`
    :param bibfile: The bib file name.
    :type bibfile: ``str``
    :return: The parsed bibliography data.
    :rtype: :class:`pybtex.database.BibliographyData`
    """
    parser = bibtex.Parser()
    app.info(bold("parsing bibtex file {0}... ".format(bibfile)), nonl=True)
    parser.parse_file(bibfile)
    app.info("parsed {0} entries"
             .format(len(parser.data.entries)))
    return parser.data

def update_bibfile_info(app, bibfile, mtime):
    """Parse *bibfile* (see :func:`parse_bibfile`), and store the
    parsed data, along with modification time *mtime*, in the bibtex
    cache.

    :param app: The :mod:`sphinx application <sphinx.application>`.
    :type app: :class:`sphinx.application.Sphinx`
    :param bibfile: The bib file name.
    :type bibfile: ``str``
    :param mtime: The bib file's modification time.
    :type mtime: ``float``
    """
    cache = app.env.bibtex_info.bibfiles
    cache[bibfile] = BibfileInfo(
        mtime=mtime,
        data=parse_bibfile(app, bibfile))

def process_bibfile(app, bibfile):
    """Check if ``app.env.bibtex_info.bibfiles[bibfile]`` is still
    up-to-date. If not, parse the *bibfile* (see
    :func:`update_bibfile_info`), and store parsed data in the bibtex
    cache.

    :param app: The :mod:`sphinx application <sphinx.application>`.
    :type app: :class:`sphinx.application.Sphinx`
    :param bibfile: The bib file name.
    :type bibfile: ``str``
    """
    cache = app.env.bibtex_info.bibfiles
    # get modification time of bibfile
    try:
        mtime = os.path.getmtime(bibfile)
    except OSError:
        app.warn(
            standout("could not open bibtex file {0}.".format(bibfile)))
        cache[bibfile] = {
            "mtime": -float('inf'),
            "data": {}}
        return
    # get cache and check if it is still up to date
    # if it is not up to date, parse the bibtex file
    # and store it in the cache
    app.info(bold("checking for {0} in bibtex cache... ".format(bibfile)),
             nonl=True)
    try:
        bibfile_cache = cache[bibfile]
    except KeyError:
        app.info("not found")
        update_bibfile_info(app, bibfile, mtime)
    else:
        if mtime != bibfile_cache.mtime:
            app.info("out of date")
            update_bibfile_info(app, bibfile, mtime)
        else:
            app.info('up to date')

def init_bibtex_info(app):
    """Create ``app.env.bibtex_info`` if it does not exist yet.

    :param app: The :mod:`sphinx application <sphinx.application>`.
    :type app: :class:`sphinx.application.Sphinx`
    """
    if not hasattr(app.env, "bibtex_info"):
        app.env.bibtex_info = BibtexInfo()

def purge_bibtex_info(app, env, docname):
    """Remove all information related to *docname* from the cache."""

    cache = env.bibtex_info.bibliographies
    ids = [id_ for id_, info in cache.iteritems()
           if info.docname == docname]
    for id_ in ids:
        del cache[id_]

def process_bibliography_nodes(app, doctree, docname):
    """Replace bibliography nodes by list of references."""

    for bibnode in doctree.traverse(bibliography):
        # get the information of this bibliography node
        # by looking up its id in the bibliography cache
        id_ = bibnode['ids'][0]
        info = [info for other_id, info
                in app.env.bibtex_info.bibliographies.iteritems()
                if other_id == id_][0]
        # TODO handle the actual citations, for now just print .bib file names
        bibnode.replace_self(
            [nodes.inline(" ".join(info.bibfiles),
                          " ".join(info.bibfiles))])

def process_cite_nodes(app, doctree, docname):
    """Replace cite nodes by footnote or citation nodes."""

    for citenode in doctree.traverse(cite):
        # TODO handle the actual citations
        citenode.replace_self([])

def setup(app):
    """Set up the bibtex extension:

    * register directives
    * register nodes
    * register roles
    * connect events to functions
    """

    app.add_directive("bibliography", BibliographyDirective)
    app.add_node(bibliography)
    app.add_node(cite)
    app.add_role("cite", XRefRole())
    app.connect("builder-inited", init_bibtex_info)
    app.connect("doctree-resolved", process_bibliography_nodes)
    app.connect("doctree-resolved", process_cite_nodes)
    app.connect("env-purge-doc", purge_bibtex_info)
