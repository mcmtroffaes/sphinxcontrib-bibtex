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
from sphinx.util.console import standout

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
    """Process cite nodes by replacing them with their label and
    updating their footnote_reference parent refid.

    :param app: The sphinx application.
    :type app: :class:`sphinx.application.Sphinx`
    :param doctree: The document tree.
    :type doctree: :class:`docutils.nodes.document`
    :param docname: The document name.
    :type docname: :class:`str`
    """
    for citenode in doctree.traverse(cite):
        # citation key occurs as contents (text) of the citenode
        key = citenode.astext()
        # create reference id (using the same method as in pybtex)
        refid = docutils.nodes.make_id("bibtex-cite-%s" % key)
        # cite nodes always have a footnote_reference as parent
        # (as defined by their role, see the setup function,
        # the add_role("cite", ...) call)
        footnote_reference_node = citenode.parent
        footnote_reference_node['refid'] = refid
        # find the reference label and set the label text
        # by inspecting all bibliography directives
        # and all bibfiles contained in them
        label = None
        for info in app.env.bibtex_cache.bibliographies.itervalues():
            for bibfile in info.bibfiles:
                data = app.env.bibtex_cache.bibfiles[bibfile].data
                if key in data.entries:
                    # key found!
                    if label is None:
                        entry = data.entries[key]
                        # locate and instantiate style plugin
                        style_cls = find_plugin(
                            'pybtex.style.formatting', info.style)
                        style = style_cls()
                        label = style.format_label(entry)
                    else:
                        app.warn(
                            standout("multiple entries for bibtex key {0}."
                                     .format(key)))
        if label is None:
            app.warn(
                standout("bibtex key {0} not found in any bibtex file."
                         .format(key)))
            label = '?'
        citenode.replace_self([docutils.nodes.inline(label, label)])

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
    app.add_role("cite",
        XRefRole(
            nodeclass=docutils.nodes.footnote_reference,
            innernodeclass=cite))
    app.connect("builder-inited", init_bibtex_cache)
    app.connect("doctree-resolved", process_bibliography_nodes)
    app.connect("doctree-resolved", process_cite_nodes)
    app.connect("env-purge-doc", purge_bibtex_cache)
