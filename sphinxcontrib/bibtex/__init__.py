# -*- coding: utf-8 -*-
"""
    Sphinx Interface
    ~~~~~~~~~~~~~~~~

    .. autofunction:: setup
    .. autofunction:: init_bibtex_cache
    .. autofunction:: purge_bibtex_cache
    .. autofunction:: process_citations
    .. autofunction:: process_citation_references
    .. autofunction:: check_duplicate_labels
"""

import docutils.nodes
import docutils.parsers.rst
from sphinxcontrib.bibtex.cache import Cache
from sphinxcontrib.bibtex.nodes import bibliography
from sphinxcontrib.bibtex.roles import CiteRole
from sphinxcontrib.bibtex.directives import BibliographyDirective
from sphinxcontrib.bibtex.transforms import BibliographyTransform
import six


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
        key = node[0].astext()
        try:
            label = app.env.bibtex_cache.get_label_from_key(key)
        except KeyError:
            app.warn("could not relabel citation [%s]" % key)
        else:
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
        # exclude sphinx [source] labels
        if isinstance(node[0], docutils.nodes.Element):
            if 'viewcode-link' in node[0]['classes']:
                continue
        text = node[0].astext()
        if text.startswith('[') and text.endswith(']'):
            key = text[1:-1]
            try:
                label = app.env.bibtex_cache.get_label_from_key(key)
            except KeyError:
                app.warn("could not relabel citation reference [%s]" % key)
            else:
                node[0] = docutils.nodes.Text('[' + label + ']')


def check_duplicate_labels(app, env):
    """Check and warn about duplicate citation labels.

    :param app: The sphinx application.
    :type app: :class:`sphinx.application.Sphinx`
    :param env: The sphinx build environment.
    :type env: :class:`sphinx.environment.BuildEnvironment`
    """
    label_to_key = {}
    for info in env.bibtex_cache.get_all_bibliography_caches():
        for key, label in six.iteritems(info.labels):
            if label in label_to_key:
                app.warn(
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

    # docutils keeps state around during testing, so to avoid spurious
    # warnings, we detect here whether the directives have already been
    # registered... very ugly hack but no better solution so far
    _directives = docutils.parsers.rst.directives._directives
    if "bibliography" not in _directives:
        app.add_directive("bibliography", BibliographyDirective)
        app.add_role("cite", CiteRole())
        app.add_node(bibliography)
        app.add_transform(BibliographyTransform)
    else:
        assert _directives["bibliography"] is BibliographyDirective

    # Parallel read is not safe at the moment: in the current design,
    # the document that contains references must be read last for all
    # references to be resolved.
    return {'parallel_read_safe': False}
