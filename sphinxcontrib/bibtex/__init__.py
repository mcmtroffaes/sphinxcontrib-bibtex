# -*- coding: utf-8 -*-
"""
    .. autofunction:: setup
    .. autofunction:: init_bibtex_cache
    .. autofunction:: purge_bibtex_cache
    .. autofunction:: process_citations
    .. autofunction:: process_citation_references
    .. autofunction:: check_duplicate_labels
"""

import docutils.nodes
import sphinx.util
from .cache import Cache
from .nodes import bibliography
from .roles import CiteRole
from .directives import BibliographyDirective
from .transforms import BibliographyTransform


logger = sphinx.util.logging.getLogger(__name__)


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


def process_citations(app, doctree, docname):
    """Replace labels of citation nodes by actual labels.

    :param app: The sphinx application.
    :type app: :class:`sphinx.application.Sphinx`
    :param doctree: The document tree.
    :type doctree: :class:`docutils.nodes.document`
    :param docname: The document name.
    :type docname: :class:`str`
    """
    for node in doctree.traverse(docutils.nodes.citation):
        if "bibtex" in node.attributes.get('classes', []):
            key = node[0].astext()
            label = app.env.bibtex_cache.get_label_from_key(key)
            node[0] = docutils.nodes.label('', label)


def process_citation_references(app, doctree, docname):
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
    for node in doctree.traverse(docutils.nodes.reference):
        if "bibtex" in node.attributes.get('classes', []):
            text = node[0].astext()
            key = text[1:-1]
            label = app.env.bibtex_cache.get_label_from_key(key)
            node[0] = docutils.nodes.Text('[' + label + ']')


def check_duplicate_labels(app, env):
    """Check and warn about duplicate citation labels.

    :param app: The sphinx application.
    :type app: :class:`sphinx.application.Sphinx`
    :param env: The sphinx build environment.
    :type env: :class:`sphinx.environment.BuildEnvironment`
    """
    label_to_key = {}
    for bibcaches in env.bibtex_cache.bibliographies.values():
        for bibcache in bibcaches.values():
            for key, label in bibcache.labels.items():
                if label in label_to_key:
                    logger.warning(
                        "duplicate label for keys %s and %s"
                        % (key, label_to_key[label]))
                else:
                    label_to_key[label] = key


def setup(app):
    """Set up the bibtex extension:

    * register config values
    * register directives
    * register nodes
    * register roles
    * register transforms
    * connect events to functions

    :param app: The sphinx application.
    :type app: :class:`sphinx.application.Sphinx`
    """

    app.add_config_value("bibtex_default_style", "alpha", "html")
    app.connect("builder-inited", init_bibtex_cache)
    app.connect("doctree-resolved", process_citations)
    app.connect("doctree-resolved", process_citation_references)
    app.connect("env-purge-doc", purge_bibtex_cache)
    app.connect("env-updated", check_duplicate_labels)
    app.add_directive("bibliography", BibliographyDirective)
    app.add_role("cite", CiteRole())
    app.add_node(bibliography, override=True)
    app.add_transform(BibliographyTransform)

    # Parallel read is not safe at the moment: in the current design,
    # the document that contains references must be read last for all
    # references to be resolved.
    return {
        'env_version': 1,
        'parallel_read_safe': False,
        'parallel_write_safe': True,
        }
