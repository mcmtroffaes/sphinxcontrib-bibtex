"""
    .. autoclass:: BibliographyTransform
        :show-inheritance:

        .. autoattribute:: default_priority
        .. automethod:: run

    .. autofunction:: node_text_transform

    .. autofunction:: transform_url_command
"""
from typing import cast

import docutils.nodes
import docutils.transforms
import sphinx.util

from pybtex.plugin import find_plugin
from sphinx.transforms.post_transforms import SphinxPostTransform

from .cache import BibtexDomain
from .nodes import bibliography


logger = sphinx.util.logging.getLogger(__name__)


def node_text_transform(node, transform):
    """Apply transformation to all Text nodes within node."""
    for child in node.children:
        if isinstance(child, docutils.nodes.Text):
            node.replace(child, transform(child))
        else:
            node_text_transform(child, transform)


def transform_url_command(textnode):
    """Convert '\\\\url{...}' into a proper docutils hyperlink."""
    text = textnode.astext()
    if '\\url' in text:
        text1, _, text = text.partition('\\url')
        text2, _, text3 = text.partition('}')
        text2 = text2.lstrip(' {')
        ref = docutils.nodes.reference(refuri=text2)
        ref += docutils.nodes.Text(text2)
        node = docutils.nodes.inline()
        node += transform_url_command(docutils.nodes.Text(text1))
        node += ref
        node += transform_url_command(docutils.nodes.Text(text3))
        return node
    else:
        return textnode


def get_docnames(env):
    rel = env.collect_relations()
    docname = env.config.master_doc
    while docname is not None:
        yield docname
        parent, prevdoc, nextdoc = rel[docname]
        docname = nextdoc


class BibliographyTransform(SphinxPostTransform):
    """A docutils transform to generate citation entries for
    bibliography nodes.
    """

    # transform must be applied before sphinx runs its ReferencesResolver
    # which has priority 10, so when ReferencesResolver calls the cite domain
    # resolve_xref, the target is present and all will work fine
    default_priority = 5

    def run(self, **kwargs):
        """Transform each
        :class:`~sphinxcontrib.bibtex.nodes.bibliography` node into a
        list of citations.
        """
        env = self.document.settings.env
        docnames = list(get_docnames(env))
        for bibnode in self.document.traverse(bibliography):
            domain = cast(BibtexDomain, env.get_domain('cite'))
            id_ = bibnode['ids'][0]
            bibcache = domain.bibliographies[id_]
            entries = domain.get_bibliography_entries(
                id_=id_, warn=logger.warning, docnames=docnames)
            # locate and instantiate style and backend plugins
            style = find_plugin('pybtex.style.formatting', bibcache.style)()
            backend = find_plugin('pybtex.backends', 'docutils')()
            # create citation nodes for all references
            if bibcache.list_ == "enumerated":
                nodes = docutils.nodes.enumerated_list()
                nodes['enumtype'] = bibcache.enumtype
                if bibcache.start >= 1:
                    nodes['start'] = bibcache.start
                    domain.enum_count[env.docname] = bibcache.start
                else:
                    nodes['start'] = domain.enum_count[env.docname]
            elif bibcache.list_ == "bullet":
                nodes = docutils.nodes.bullet_list()
            else:  # "citation"
                nodes = docutils.nodes.paragraph()
            # remind: style.format_entries modifies entries in unpickable way
            for entry in style.format_entries(entries):
                if bibcache.list_ in ["enumerated", "bullet"]:
                    citation = docutils.nodes.list_item()
                    citation += backend.paragraph(entry)
                else:  # "citation"
                    citation = backend.citation(entry, self.document)
                    citation['classes'].append('bibtex')
                    # backend.citation(...) uses entry.key as citation label
                    # we change it to entry.label later onwards
                    # but we must note the entry.label now;
                    # at this point, we also already prefix the label
                    key = bibcache.keyprefix + entry.key
                    label = '[' + bibcache.labelprefix + entry.label + ']'
                    domain.citations[key] = (
                        env.docname, citation['ids'][0], label)
                    # citation[0] is the label node
                    # we override it to change the text
                    assert isinstance(citation[0], docutils.nodes.label)
                    citation[0] = docutils.nodes.label(label, label)
                node_text_transform(citation, transform_url_command)
                nodes += citation
                if bibcache.list_ == "enumerated":
                    domain.enum_count[env.docname] += 1
            if env.bibtex_bibliography_header is not None:
                nodes = [env.bibtex_bibliography_header.deepcopy(), nodes]
            bibnode.replace_self(nodes)
