# -*- coding: utf-8 -*-
"""
    .. autofunction:: setup
    .. autofunction:: init_footbib_cache
    .. autofunction:: purge_footbib_cache
    .. autofunction:: merge_footbib_cache
"""

import docutils.frontend
import docutils.parsers.rst
import docutils.utils
import re
import sphinx.util
from sphinx.errors import ExtensionError
from .bibfile import normpath_bibfile, process_bibfile
from .foot_cache import Cache
from .foot_nodes import bibliography
from .foot_roles import CiteRole
from .foot_directives import BibliographyDirective
from .foot_transforms import BibliographyTransform


logger = sphinx.util.logging.getLogger(__name__)


def init_footbib_cache(app):
    """Create ``app.env.footbib_cache`` if it does not exist yet.

    :param app: The sphinx application.
    :type app: :class:`sphinx.application.Sphinx`
    """
    # check config
    if not app.config.bibtex_bibfiles:
        raise ExtensionError("You must configure the bibtex_bibfiles setting")
    # add cache if not already present
    if not hasattr(app.env, "footbib_cache"):
        app.env.footbib_cache = Cache()
    if not hasattr(app.env, "bibtex_bibfiles"):
        app.env.bibtex_bibfiles = {}
    # update bib file information in the cache
    for bibfile in app.config.bibtex_bibfiles:
        process_bibfile(
            app.env.bibtex_bibfiles,
            normpath_bibfile(app.env, bibfile, app.config.master_doc),
            app.config.bibtex_encoding)
    # parse footbibliography header
    if not hasattr(app.env, "bibtex_footbibliography_header"):
        parser = docutils.parsers.rst.Parser()
        settings = docutils.frontend.OptionParser(
            components=(docutils.parsers.rst.Parser,)).get_default_values()
        document = docutils.utils.new_document(
            "footbibliography_header", settings)
        parser.parse(app.config.bibtex_footbibliography_header, document)
        app.env.bibtex_footbibliography_header = (
            document[0] if len(document) > 0 else None)


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

    app.add_config_value("bibtex_style", "alpha", "html")
    app.add_config_value("bibtex_bibfiles", [], "html")
    app.add_config_value("bibtex_encoding", "utf-8-sig", "html")
    app.add_config_value("bibtex_footbibliography_header", "", "html")
    app.connect("builder-inited", init_footbib_cache)
    app.connect("env-merge-info", merge_footbib_cache)
    app.connect("env-purge-doc", purge_footbib_cache)
    app.connect("source-read", init_current_id)
    app.add_directive("footbibliography", BibliographyDirective)
    app.add_role("footcite", CiteRole())
    app.add_node(bibliography, override=True)
    app.add_transform(BibliographyTransform)

    return {
        'env_version': 1,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
        }
