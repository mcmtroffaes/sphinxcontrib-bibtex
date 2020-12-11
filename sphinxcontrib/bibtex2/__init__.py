# -*- coding: utf-8 -*-
"""
    .. autofunction:: setup
    .. autofunction:: init_bibtex_cache
"""

import docutils.frontend
import docutils.parsers.rst
import docutils.utils
import sphinx.util
from .foot_nodes import bibliography
from .foot_roles import FootCiteRole
from .foot_directives import FootBibliographyDirective
from .foot_transforms import FootBibliographyTransform


logger = sphinx.util.logging.getLogger(__name__)


def init_bibtex_cache(app):
    """Initialize the extension cache.

    :param app: The sphinx application.
    :type app: :class:`sphinx.application.Sphinx`
    """
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


def init_current_id(app, docname, source):
    app.env.bibtex_cache.new_foot_current_id(app.env)


def setup(app):
    """Set up the bibtex2 extension:

    * register config values
    * register directives
    * register nodes
    * register roles
    * register transforms
    * connect events to functions

    :param app: The sphinx application.
    :type app: :class:`sphinx.application.Sphinx`
    """

    app.add_config_value("bibtex_footbibliography_header", "", "html")
    app.connect("builder-inited", init_bibtex_cache)
    app.connect("source-read", init_current_id)
    app.add_directive("footbibliography", FootBibliographyDirective)
    app.add_role("footcite", FootCiteRole())
    app.add_node(bibliography, override=True)
    app.add_transform(FootBibliographyTransform)

    return {
        'env_version': 2,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
        }
