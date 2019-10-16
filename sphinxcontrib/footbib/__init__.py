# -*- coding: utf-8 -*-
"""
    .. autofunction:: setup
    .. autofunction:: init_footbib_cache
    .. autofunction:: purge_footbib_cache
    .. autofunction:: merge_footbib_cache
"""

import re
import sphinx.util
from sphinx.errors import ExtensionError
from ..bibtex.cache import normpath_bibfile, process_bibfile
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
    # check config
    if not app.config.footbib_bibfiles:
        raise ExtensionError("You must configure the footbib_bibfiles setting")
    # add cache if not already present
    if not hasattr(app.env, "footbib_cache"):
        app.env.footbib_cache = Cache()
    # update bib file information in the cache
    for bibfile in app.config.footbib_bibfiles:
        process_bibfile(
            app.env.footbib_cache.bibfiles,
            normpath_bibfile(app.env, bibfile),
            app.config.footbib_encoding)


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


def add_footbibliography(app, docname, source):
    """Add a footer containing a single footbibliography directive, if
    need be.

    :param app: The sphinx application.
    :type app: :class:`sphinx.application.Sphinx`
    :param docname: The document name.
    :type docname: :class:`str`
    :param source: The source, as a list containing a single string.
    :type source: :class:`list`
    """

    before, _, after = source[0].rpartition("footbibliography::")
    cites_before = set(re.findall(":footcite:`[^`]*`", before))
    cites_after = set(re.findall(":footcite:`[^`]*`", after))
    if cites_after - cites_before:
        source[0] += app.config.footbib_footer


def init_current_id(app, docname, source):
    app.env.footbib_cache.new_current_id(app.env)


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
    app.add_config_value("footbib_bibfiles", [], "html")
    app.add_config_value("footbib_encoding", "utf-8-sig", "html")
    app.add_config_value(
        "footbib_footer", "\n\n.. footbibliography::\n", "html")
    app.connect("builder-inited", init_footbib_cache)
    app.connect("env-merge-info", merge_footbib_cache)
    app.connect("env-purge-doc", purge_footbib_cache)
    app.connect("source-read", add_footbibliography)
    app.connect("source-read", init_current_id)
    app.add_directive("footbibliography", BibliographyDirective)
    app.add_role("footcite", CiteRole())
    app.add_node(bibliography, override=True)
    app.add_transform(BibliographyTransform)

    return {'parallel_read_safe': True}
