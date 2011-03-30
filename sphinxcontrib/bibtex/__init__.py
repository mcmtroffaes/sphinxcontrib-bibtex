# -*- coding: utf-8 -*-
"""
    Sphinx Interface
    ~~~~~~~~~~~~~~~~

    .. autofunction:: setup
    .. autofunction:: init_bibtex_cache
    .. autofunction:: purge_bibtex_cache
    .. autofunction:: process_bibliography_nodes
    .. autofunction:: process_cite_nodes
"""

import docutils.nodes
from sphinx.roles import XRefRole # for :cite:

from pybtex.backends.doctree import Backend as output_backend
from pybtex.plugin import find_plugin

from sphinxcontrib.bibtex.cache import Cache, BibfileCache, BibliographyCache
from sphinxcontrib.bibtex.nodes import bibliography, cite
from sphinxcontrib.bibtex.directives import BibliographyDirective

def init_bibtex_cache(app):
    """Create ``app.env.bibtex_cache`` if it does not exist yet.

    :param app: The sphinx application.
    :type app: :class:`sphinx.application.Sphinx`
    """
    if not hasattr(app.env, "bibtex_cache"):
        app.env.bibtex_cache = Cache()

def purge_bibtex_cache(app, env, docname):
    """Remove all information related to *docname* from the cache.

    :param app: The sphinx application.
    :type app: :class:`sphinx.application.Sphinx`
    :param env: The sphinx build environment.
    :type env: :class:`sphinx.environment.BuildEnvironment`
    """
    env.bibtex_cache.purge(docname)

def process_bibliography_nodes(app, doctree, docname):
    """Replace bibliography nodes by list of references.

    :param app: The sphinx application.
    :type app: :class:`sphinx.application.Sphinx`
    :param doctree: The document tree.
    :type doctree: :class:`docutils.nodes.document`
    :param docname: The document name.
    :type docname: :class:`str`
    """
    for bibnode in doctree.traverse(bibliography):
        # get the information of this bibliography node
        # by looking up its id in the bibliography cache
        id_ = bibnode['ids'][0]
        info = [info for other_id, info
                in app.env.bibtex_cache.bibliographies.iteritems()
                if other_id == id_][0]
        # TODO for now, simply generate *all* entries in the .bib files
        citations = []
        # locate and instantiate style plugin
        style_cls = find_plugin(
            'pybtex.style.formatting', info.style)
        style = style_cls()
        for bibfile in info.bibfiles:
            # format all entries
            data = app.env.bibtex_cache.bibfiles[bibfile].data
            formatted_entries = style.format_entries(data.entries.itervalues())
            output_backend().write_to_doctree(
                formatted_entries, citations)
        # XXX this is a hack: docutils throws an exception if we
        # XXX replace_self([]) for nodes that have an 'ids' attribute
        # XXX (such as bibnode)
        if not citations:
            citations.append(docutils.nodes.inline("", ""))
        bibnode.replace_self(citations)

def process_cite_nodes(app, doctree, docname):
    """Replace cite nodes by footnote or citation nodes.

    :param app: The sphinx application.
    :type app: :class:`sphinx.application.Sphinx`
    :param doctree: The document tree.
    :type doctree: :class:`docutils.nodes.document`
    :param docname: The document name.
    :type docname: :class:`str`
    """

    #for citenode in doctree.traverse(cite):
        # TODO handle the actual citations
        #citenode.replace_self([])

def setup(app):
    """Set up the bibtex extension:

    * register directives
    * register nodes
    * register roles
    * connect events to functions

    :param app: The sphinx application.
    :type app: :class:`sphinx.application.Sphinx`
    """

    app.add_directive("bibliography", BibliographyDirective)
    app.add_node(bibliography)
    app.add_node(cite)
    app.add_role("cite", XRefRole())
    app.connect("builder-inited", init_bibtex_cache)
    app.connect("doctree-resolved", process_bibliography_nodes)
    app.connect("doctree-resolved", process_cite_nodes)
    app.connect("env-purge-doc", purge_bibtex_cache)
