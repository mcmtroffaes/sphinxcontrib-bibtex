# -*- coding: utf-8 -*-
"""
    .. autofunction:: setup
    .. autofunction:: init_footbib_cache
    .. autofunction:: purge_footbib_cache
    .. autofunction:: merge_footbib_cache
"""

import sphinx.util
from .cache import Cache
from .nodes import bibliography
from .roles import CiteRole
from .directives import BibliographyDirective
from .transforms import BibliographyTransform


logger = sphinx.util.logging.getLogger(__name__)


def init_footbib_cache(app):
    """Create ``app.env.footbib_cache`` if it does not exist yet.

    :param app: The sphinx application.
    :type app: :class:`sphinx.application.Sphinx`
    """
    if not hasattr(app.env, "footbib_cache"):
        app.env.footbib_cache = Cache()


def purge_footbib_cache(app, env, docname):
    """Remove all information related to *docname* from the cache.

    :param app: The sphinx application.
    :type app: :class:`sphinx.application.Sphinx`
    :param env: The sphinx build environment.
    :type env: :class:`sphinx.environment.BuildEnvironment`
    """
    env.footbib_cache.purge(docname)


def merge_footbib_cache(app, env, docnames, other):
    """Merge environment information related to *docnames*.

    :param app: The sphinx application.
    :type app: :class:`sphinx.application.Sphinx`
    :param env: The sphinx build environment.
    :type env: :class:`sphinx.environment.BuildEnvironment`
    :param docnames: The document names.
    :type docnames: :class:`str`
    :param other: The other environment.
    :type other: :class:`sphinx.environment.BuildEnvironment`
    """
    env.footbib_cache.merge(docnames, other.footbib_cache)


def setup(app):
    """Set up the footbib extension:

    * register config values
    * register directives
    * register nodes
    * register roles
    * register transforms
    * connect events to functions

    :param app: The sphinx application.
    :type app: :class:`sphinx.application.Sphinx`
    """

    app.add_config_value("footbib_default_style", "alpha", "html")
    app.connect("builder-inited", init_footbib_cache)
    app.connect("env-merge-info", merge_footbib_cache)
    app.connect("env-purge-doc", purge_footbib_cache)
    app.add_directive("footbibliography", BibliographyDirective)
    app.add_role("footcite", CiteRole())
    app.add_node(bibliography, override=True)
    app.add_transform(BibliographyTransform)

    return {'parallel_read_safe': True}
