"""
    New Doctree Directives
    ~~~~~~~~~~~~~~~~~~~~~~

    .. autoclass:: BibliographyDirective

        .. automethod:: run
        .. automethod:: process_bibfile
        .. automethod:: update_bibfile_cache
        .. automethod:: parse_bibfile
"""

import os.path # getmtime()

import copy # deepcopy
import docutils.nodes
from docutils.parsers.rst import directives # for Directive.option_spec
from sphinx.util.compat import Directive
from sphinx.util.console import bold, standout

from pybtex.backends.doctree import Backend as output_backend
from pybtex.database.input import bibtex
from pybtex.plugin import find_plugin

from sphinxcontrib.bibtex.cache import BibliographyCache, BibfileCache
import sphinxcontrib.bibtex.latex_codec # registers the latex codec

def node_text_transform(node, transform):
    """Apply transformation to all Text nodes within node."""
    for child in node.children:
        if isinstance(child, docutils.nodes.Text):
            node.replace(child, transform(child))
        else:
            node_text_transform(child, transform)

def transform_curly_bracket_strip(textnode):
    """Strip curly brackets from text."""
    text = textnode.astext()
    text.replace('{', '').replace('}', '')
    return docutils.nodes.Text(text)

def transform_url_command(textnode):
    """Convert '\url{...}' into a proper docutils hyperlink."""
    # XXX for now, this just converts a single \url command
    # XXX should use re.finditer or something similar
    text = textnode.astext()
    if '\url' in text:
        text1, _, text = text.partition('\url')
        text2, _, text3 = text.partition('}')
        text2 = text2.lstrip(' {')
        ref = docutils.nodes.reference(refuri=text2)
        ref += docutils.nodes.Text(text2)
        node = docutils.nodes.inline()
        node += docutils.nodes.Text(text1)
        node += ref
        node += docutils.nodes.Text(text3)
        return node
    else:
        return textnode

class BibliographyDirective(Directive):
    """Class for processing the :rst:dir:`bibliography` directive."""

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = False
    option_spec = {
        'cited': directives.flag,
        'notcited': directives.flag,
        'all': directives.flag,
        'style': directives.unchanged,
        'encoding': directives.encoding,
        'disable-curly-bracket-strip': directives.flag,
    }

    def run(self):
        """Process .bib files, set file dependencies, and create a
        nodes for all entries of the bibliography.
        """
        env = self.state.document.settings.env
        cache = env.bibtex_cache.bibliographies
        # create id and cache for this node
        # this id will be stored with the node
        # and is used to look up additional data in env.bibtex_cache
        id_ = 'bibtex-bibliography-%s' % env.new_serialno('bibtex')
        info = BibliographyCache(
            docname=env.docname,
            cite=(
                "all"
                if "all" in self.options else (
                    "notcited"
                    if "notcited" in self.options else (
                        "cited"))),
            style=self.options.get("style", "unsrt"),
            encoding=self.options.get(
                'encoding',
                'latex+' + self.state.document.settings.input_encoding),
            curly_bracket_strip=(
                'disable-curly-bracket-strip' not in self.options),
            )
        cache[id_] = info
        # get all bibfiles, and generate entries
        entries = []
        for bibfile in self.arguments[0].split():
            # convert to relative path to ensure that the same file
            # only occurs once in the cache
            bibfile = env.relfn2path(bibfile.strip())[0]
            data = self.process_bibfile(bibfile, info.encoding)
            # XXX entries are modified below in an unpickable way
            # XXX so fetch a deep copy
            entries += copy.deepcopy(list(data.entries.itervalues()))
            env.note_dependency(bibfile)
            info.bibfiles.append(bibfile)
        # locate and instantiate style plugin
        style_cls = find_plugin(
            'pybtex.style.formatting', info.style)
        style = style_cls()
        # create citation nodes for all references
        nodes = []
        backend = output_backend()
        # XXX style.format_entries modifies entries in unpickable way
        for entry in style.format_entries(entries):
            citation = backend.citation(entry, self.state.document)
            node_text_transform(citation, transform_url_command)
            if info.curly_bracket_strip:
                node_text_transform(citation, transform_curly_bracket_strip)
            nodes.append(citation)
        return nodes

    def parse_bibfile(self, bibfile, encoding):
        """Parse *bibfile*, and return parsed data.

        :param bibfile: The bib file name.
        :type bibfile: ``str``
        :return: The parsed bibliography data.
        :rtype: :class:`pybtex.database.BibliographyData`
        """
        app = self.state.document.settings.env.app
        parser = bibtex.Parser(encoding)
        app.info(
            bold("parsing bibtex file {0}... ".format(bibfile)), nonl=True)
        parser.parse_file(bibfile)
        app.info("parsed {0} entries"
                 .format(len(parser.data.entries)))
        return parser.data

    def update_bibfile_cache(self, bibfile, mtime, encoding):
        """Parse *bibfile* (see :meth:`parse_bibfile`), and store the
        parsed data, along with modification time *mtime*, in the
        bibtex cache.

        :param bibfile: The bib file name.
        :type bibfile: ``str``
        :param mtime: The bib file's modification time.
        :type mtime: ``float``
        :return: The parsed bibliography data.
        :rtype: :class:`pybtex.database.BibliographyData`
        """
        data = self.parse_bibfile(bibfile, encoding)
        env = self.state.document.settings.env
        env.bibtex_cache.bibfiles[bibfile] = BibfileCache(
            mtime=mtime,
            data=data)
        return data

    def process_bibfile(self, bibfile, encoding):
        """Check if ``env.bibtex_cache.bibfiles[bibfile]`` is still
        up to date. If not, parse the *bibfile* (see
        :meth:`update_bibfile_cache`), and store parsed data in the
        bibtex cache.

        :param bibfile: The bib file name.
        :type bibfile: ``str``
        :return: The parsed bibliography data.
        :rtype: :class:`pybtex.database.BibliographyData`
        """
        env = self.state.document.settings.env
        cache = env.bibtex_cache.bibfiles
        # get modification time of bibfile
        try:
            mtime = os.path.getmtime(bibfile)
        except OSError:
            env.app.warn(
                standout("could not open bibtex file {0}.".format(bibfile)))
            cache[bibfile] = BibfileCache() # dummy cache
            return cache[bibfile].data
        # get cache and check if it is still up to date
        # if it is not up to date, parse the bibtex file
        # and store it in the cache
        env.app.info(
            bold("checking for {0} in bibtex cache... ".format(bibfile)),
            nonl=True)
        try:
            bibfile_cache = cache[bibfile]
        except KeyError:
            env.app.info("not found")
            self.update_bibfile_cache(bibfile, mtime, encoding)
        else:
            if mtime != bibfile_cache.mtime:
                env.app.info("out of date")
                self.update_bibfile_cache(bibfile, mtime, encoding)
            else:
                env.app.info('up to date')
        return cache[bibfile].data
