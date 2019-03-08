"""
    New Doctree Transforms
    ~~~~~~~~~~~~~~~~~~~~~~

    .. autoclass:: BibliographyTransform
        :show-inheritance:

        .. autoattribute:: default_priority
        .. automethod:: apply

    .. autofunction:: node_text_transform

    .. autofunction:: transform_url_command
"""

import docutils.nodes
import docutils.transforms
import sphinx.util
from sphinx import addnodes

from pybtex.plugin import find_plugin

from sphinxcontrib.bibtex.nodes import bibliography


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


class OverrideCitationReferences(docutils.transforms.Transform):
    """
    Replace citation references by pending_xref nodes before the default
    docutils transform tries to resolve them.

    This transform overrides sphinx.transforms.CitationReferences,
    in order to propogate the classes of the citation_reference node
    to the pending_xref node (see PR sphinx-doc/sphinx#6147)
    """
    # the default priority of sphinx.transforms.CitationReferences is 619
    default_priority = 618

    def apply(self, **kwargs):
        # type: (Any) -> None
        # mark citation labels as not smartquoted
        # for citation in self.document.traverse(nodes.citation):
        #     label = cast(nodes.label, citation[0])
        #     label['support_smartquotes'] = False

        for citation_ref in self.document.traverse(
                docutils.nodes.citation_reference):
            cittext = citation_ref.astext()
            refnode = addnodes.pending_xref(
                cittext, refdomain='std', reftype='citation',
                reftarget=cittext, refwarn=True,
                support_smartquotes=False,
                ids=citation_ref["ids"])
            refnode.source = citation_ref.source or citation_ref.parent.source
            refnode.line = citation_ref.line or citation_ref.parent.line
            refnode += docutils.nodes.Text('[' + cittext + ']')
            for class_name in citation_ref.attributes.get('classes', []):
                refnode.set_class(class_name)
            citation_ref.parent.replace(citation_ref, refnode)


class HandleMissingCitesTransform(docutils.transforms.Transform):
    """ before sphinx.transforms.post_transforms.ReferencesResolver
    missing citations need to be handled (default_priority=10)
    """
    default_priority = 9

    def apply(self):
        # type: () -> None
        app = self.document.settings.env.app
        for node in self.document.traverse(addnodes.pending_xref):
            if "bibtex" not in node.attributes.get('classes', []):
                continue
            text = node[0].astext()
            key = text[1:-1]
            try:
                app.env.bibtex_cache.get_label_from_key(key)
            except KeyError:
                logger.warning(
                    "could not relabel citation reference [%s]" % key)
                # strip class (otherwise ReferencesResolver fails)
                node.attributes['classes'] = []


class BibliographyTransform(docutils.transforms.Transform):

    """A docutils transform to generate citation entries for
    bibliography nodes.
    """

    # transform must be applied before references are resolved
    default_priority = 10
    """Priority of the transform. See
    http://docutils.sourceforge.net/docs/ref/transforms.html
    """

    def apply(self):
        """Transform each
        :class:`~sphinxcontrib.bibtex.nodes.bibliography` node into a
        list of citations.
        """
        env = self.document.settings.env
        docname = env.docname
        for bibnode in self.document.traverse(bibliography):
            id_ = bibnode['ids'][0]
            bibcache = env.bibtex_cache.get_bibliography_cache(
                docname=docname, id_=id_)
            entries = env.bibtex_cache.get_bibliography_entries(
                docname=docname, id_=id_, warn=logger.warning)
            # locate and instantiate style and backend plugins
            style = find_plugin('pybtex.style.formatting', bibcache.style)()
            backend = find_plugin('pybtex.backends', 'docutils')()
            # create citation nodes for all references
            if bibcache.list_ == "enumerated":
                nodes = docutils.nodes.enumerated_list()
                nodes['enumtype'] = bibcache.enumtype
                if bibcache.start >= 1:
                    nodes['start'] = bibcache.start
                    env.bibtex_cache.set_enum_count(
                        env.docname, bibcache.start)
                else:
                    nodes['start'] = env.bibtex_cache.get_enum_count(
                        env.docname)
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
                    citation.set_class('bibtex')
                    # backend.citation(...) uses entry.key as citation label
                    # we change it to entry.label later onwards
                    # but we must note the entry.label now;
                    # at this point, we also already prefix the label
                    key = citation[0].astext()
                    bibcache.labels[key] = bibcache.labelprefix + entry.label
                node_text_transform(citation, transform_url_command)
                nodes += citation
                if bibcache.list_ == "enumerated":
                    env.bibtex_cache.inc_enum_count(env.docname)
            bibnode.replace_self(nodes)
