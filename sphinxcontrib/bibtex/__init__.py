# -*- coding: utf-8 -*-
"""
    .. autofunction:: setup
    .. autofunction:: init_bibtex_cache
    .. autofunction:: init_foot_bibliography_id
    .. autofunction:: process_citations
    .. autofunction:: process_citation_references
    .. autofunction:: check_duplicate_labels
    .. autofunction:: save_bibtex_json
"""

import docutils.nodes
import json
import docutils.frontend
import docutils.parsers.rst
import docutils.utils
import sphinx.util

from typing import cast, Optional

from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment

from .bibfile import normpath_filename
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


logger = sphinx.util.logging.getLogger(__name__)


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


def process_citations(app: Sphinx, doctree: docutils.nodes.document,
                      docname: str) -> None:
    """Replace labels of citation nodes by actual labels."""
    domain = cast(BibtexDomain, app.env.get_domain('bibtex'))
    for node in doctree.traverse(docutils.nodes.citation):
        if "bibtex" in node.attributes.get('classes', []):
            key = node[0].astext()
            label = domain.get_label_from_key(key)
            node[0] = docutils.nodes.label('', label)


def process_citation_references(app: Sphinx, doctree: docutils.nodes.document,
                                docname: str) -> None:
    """Replace text of citation reference nodes by actual labels.

    :param app: The sphinx application.
    :type app: :class:`sphinx.application.Sphinx`
    :param doctree: The document tree.
    :type doctree: :class:`docutils.nodes.document`
    :param docname: The document name.
    :type docname: :class:`str`
    """
    # sphinx has already turned citation_reference nodes
    # into reference nodes, so iterate over reference nodes
    domain = cast(BibtexDomain, app.env.get_domain('bibtex'))
    for node in doctree.traverse(docutils.nodes.reference):
        if "bibtex" in node.attributes.get('classes', []):
            text = node[0].astext()
            key = text[1:-1]
            label = domain.get_label_from_key(key)
            node[0] = docutils.nodes.Text('[' + label + ']')


def check_duplicate_labels(app: Sphinx, env: BuildEnvironment) -> None:
    """Check and warn about duplicate citation labels."""
    domain = cast(BibtexDomain, env.get_domain('bibtex'))
    label_to_key = {}
    for bibcaches in domain.bibliographies.values():
        for bibcache in bibcaches.values():
            for key, label in bibcache.labels.items():
                if label in label_to_key:
                    logger.warning(
                        "duplicate label for keys %s and %s"
                        % (key, label_to_key[label]))
                else:
                    label_to_key[label] = key


def save_bibtex_json(app: Sphinx, exc: Optional[Exception]) -> None:
    if exc is None:
        json_filename = normpath_filename(app.env, "/bibtex.json")
        try:
            with open(json_filename) as json_file:
                json_string_old = json_file.read()
        except FileNotFoundError:
            json_string_old = json.dumps(
                {"cited": {}}, indent=4, sort_keys=True)
        domain = cast(BibtexDomain, app.env.get_domain('bibtex'))
        cited = {
            key: list(value)
            for key, value in domain.cited.items()}
        json_string_new = json.dumps(
            {"cited": cited}, indent=4, sort_keys=True)
        if json_string_old != json_string_new:
            with open(json_filename, 'w') as json_file:
                json_file.write(json_string_new)
            logger.error("""bibtex citations changed, rerun sphinx""")


def setup(app: Sphinx) -> None:
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
    app.connect("doctree-resolved", process_citations)
    app.connect("doctree-resolved", process_citation_references)
    app.connect("env-updated", check_duplicate_labels)
    app.connect("build-finished", save_bibtex_json)
    app.add_directive("bibliography", BibliographyDirective)
    app.add_role("cite", CiteRole())
    app.add_node(bibliography, override=True)
    app.add_transform(BibliographyTransform)
    app.add_directive("footbibliography", FootBibliographyDirective)
    app.add_role("footcite", FootCiteRole())
    app.add_node(footbibliography, override=True)
    app.add_transform(FootBibliographyTransform)

    return {
        'env_version': 5,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
        }
