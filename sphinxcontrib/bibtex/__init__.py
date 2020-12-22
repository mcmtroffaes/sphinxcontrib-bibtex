# -*- coding: utf-8 -*-
"""
    .. autofunction:: setup
    .. autofunction:: init_bibtex_cache
    .. autofunction:: init_foot_bibliography_id
    .. autofunction:: process_citations
    .. autofunction:: process_citation_references
    .. autofunction:: check_duplicate_labels
"""

import docutils.nodes
import docutils.frontend
import docutils.parsers.rst
import docutils.utils
import sphinx.util

from typing import cast, Any, Dict

from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment

from .cache import BibtexDomain
from .nodes import bibliography
from .roles import CiteRole
from .directives import BibliographyDirective
from .transforms import BibliographyTransform
from .foot_nodes import footbibliography
from .foot_roles import FootCiteRole
from .foot_directives import FootBibliographyDirective
from .foot_directives import new_foot_bibliography_id
from .foot_transforms import FootBibliographyTransform


def init_bibtex_cache(app: Sphinx) -> None:
    """Initialize the Sphinx build."""
    # parse bibliography headers
    for directive in ("bibliography", "footbibliography"):
        conf_name = "bibtex_{0}_header".format(directive)
        if not hasattr(app.env, conf_name):
            parser = docutils.parsers.rst.Parser()
            settings = docutils.frontend.OptionParser(
                components=(docutils.parsers.rst.Parser,)).get_default_values()
            document = docutils.utils.new_document(
                "{0}_header".format(directive), settings)
            parser.parse(getattr(app.config, conf_name), document)
            setattr(app.env, conf_name,
                    document[0] if len(document) > 0 else None)


def init_foot_bibliography_id(app: Sphinx, docname: docutils.nodes.document,
                              source: str) -> None:
    """Initialize current footbibliography id for *docname*."""
    new_foot_bibliography_id(app.env)


def setup(app: Sphinx) -> Dict[str, Any]:
    """Set up the bibtex extension:

    * register config values
    * register directives
    * register nodes
    * register roles
    * register transforms
    * connect events to functions
    """

    app.add_config_value("bibtex_default_style", "alpha", "html")
    app.add_config_value("bibtex_bibfiles", None, "html")
    app.add_config_value("bibtex_encoding", "utf-8-sig", "html")
    app.add_config_value("bibtex_bibliography_header", "", "html")
    app.add_config_value("bibtex_footbibliography_header", "", "html")
    app.add_domain(BibtexDomain)
    app.connect("builder-inited", init_bibtex_cache)
    app.connect("source-read", init_foot_bibliography_id)
    app.add_directive("bibliography", BibliographyDirective)
    app.add_role("cite", CiteRole())
    app.add_node(bibliography, override=True)
    app.add_post_transform(BibliographyTransform)
    app.add_directive("footbibliography", FootBibliographyDirective)
    app.add_role("footcite", FootCiteRole())
    app.add_node(footbibliography, override=True)
    app.add_transform(FootBibliographyTransform)

    return {
        'env_version': 5,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
        }
