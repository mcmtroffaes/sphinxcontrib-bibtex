# -*- coding: utf-8 -*-
"""
    Sphinx Interface
    ~~~~~~~~~~~~~~~~

    .. autofunction:: setup
    .. autofunction:: init_bibtex_cache
    .. autofunction:: purge_bibtex_cache
"""

from sphinxcontrib.bibtex.cache import Cache
from sphinxcontrib.bibtex.roles import CiteRole
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
    app.add_role("cite", CiteRole())
    app.connect("builder-inited", init_bibtex_cache)
    app.connect("env-purge-doc", purge_bibtex_cache)
