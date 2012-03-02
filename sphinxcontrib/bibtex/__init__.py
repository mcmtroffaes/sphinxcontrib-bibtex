# -*- coding: utf-8 -*-
"""
    Sphinx Interface
    ~~~~~~~~~~~~~~~~

    .. autofunction:: setup
    .. autofunction:: init_bibtex_cache
    .. autofunction:: purge_bibtex_cache
    .. autofunction:: process_citations
    .. autofunction:: process_citation_references
"""

import docutils.nodes
from sphinxcontrib.bibtex.cache import Cache
from sphinxcontrib.bibtex.nodes import bibliography
from sphinxcontrib.bibtex.roles import CiteRole
from sphinxcontrib.bibtex.directives import BibliographyDirective
from sphinxcontrib.bibtex.transforms import BibliographyTransform

def init_bibtex_cache(app):
    """Create ``app.env.bibtex_cache`` if it does not exist yet.
    Reset citation label dictionary.

    :param app: The sphinx application.
    :type app: :class:`sphinx.application.Sphinx`
    """
    if not hasattr(app.env, "bibtex_cache"):
        app.env.bibtex_cache = Cache()
    # XXX labels are currently not cached, always calculated on the fly
    app.env.bibtex_citation_label = {}
    # XXX same for list of cited references
    app.env.bibtex_cited = set()

def purge_bibtex_cache(app, env, docname):
    """Remove all information related to *docname* from the cache.

    :param app: The sphinx application.
    :type app: :class:`sphinx.application.Sphinx`
    :param env: The sphinx build environment.
    :type env: :class:`sphinx.environment.BuildEnvironment`
    """
    env.bibtex_cache.purge(docname)

def process_citations(app, doctree, docname):
    """Replace labels of citation nodes by numbers.

    :param app: The sphinx application.
    :type app: :class:`sphinx.application.Sphinx`
    :param doctree: The document tree.
    :type doctree: :class:`docutils.nodes.document`
    :param docname: The document name.
    :type docname: :class:`str`
    """
    for node in doctree.traverse(docutils.nodes.citation):
        label = node[0].astext()
        try:
            num = app.env.bibtex_citation_label[label]
        except KeyError:
            num = str(len(app.env.bibtex_citation_label) + 1)
            app.env.bibtex_citation_label[label] = num
        node[0] = docutils.nodes.label('', num)

def process_citation_references(app, doctree, docname):
    """Replace text of citation reference nodes by numbers.

    :param app: The sphinx application.
    :type app: :class:`sphinx.application.Sphinx`
    :param doctree: The document tree.
    :type doctree: :class:`docutils.nodes.document`
    :param docname: The document name.
    :type docname: :class:`str`
    """
    # XXX sphinx has already turned citation_reference nodes
    # XXX into reference nodes
    for node in doctree.traverse(docutils.nodes.reference):
        text = node[0].astext()
        if text.startswith('[') and text.endswith(']'):
            label = text[1:-1]
            node[0] = docutils.nodes.Text(
                '[' + app.env.bibtex_citation_label[label] + ']')

def setup(app):
    """Set up the bibtex extension:

    * register directives
    * register nodes
    * register roles
    * register transforms
    * connect events to functions

    :param app: The sphinx application.
    :type app: :class:`sphinx.application.Sphinx`
    """

    app.add_directive("bibliography", BibliographyDirective)
    app.add_role("cite", CiteRole())
    app.add_node(bibliography)
    app.add_transform(BibliographyTransform)
    app.connect("builder-inited", init_bibtex_cache)
    app.connect("doctree-resolved", process_citations)
    app.connect("doctree-resolved", process_citation_references)
    app.connect("env-purge-doc", purge_bibtex_cache)
