"""
    .. autoclass:: BibliographyDirective

        .. automethod:: run

    .. autofunction:: process_start_option
"""

import ast  # parse(), used for filter
import docutils.nodes
import sphinx.util

from typing import cast
from docutils.parsers.rst import Directive, directives
from sphinx.environment import BuildEnvironment

from .bibfile import normpath_filename
from .domain import BibliographyValue, BibtexDomain, BibliographyKey
from .nodes import bibliography as bibliography_node


logger = sphinx.util.logging.getLogger(__name__)


def process_start_option(value):
    """Process and validate the start option value
    of a :rst:dir:`bibliography` directive.
    If *value* is ``continue`` then this function returns -1,
    otherwise *value* is converted into a positive integer.
    """
    if value == "continue":
        return -1
    else:
        return directives.positive_int(value)


class BibliographyDirective(Directive):

    """Class for processing the :rst:dir:`bibliography` directive.

    Parses the bibliography files, and produces a
    :class:`~sphinxcontrib.bibtex.nodes.bibliography` node.

    .. seealso::

       Further processing of the resulting
       :class:`~sphinxcontrib.bibtex.nodes.bibliography` node is done
       by
       :class:`~sphinxcontrib.bibtex.transforms.BibliographyTransform`.
    """

    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    has_content = False
    option_spec = {
        'cited': directives.flag,
        'notcited': directives.flag,
        'all': directives.flag,
        'filter': directives.unchanged,
        'style': directives.unchanged,
        'list': directives.unchanged,
        'enumtype': directives.unchanged,
        'start': process_start_option,
        'labelprefix': directives.unchanged,
        'keyprefix': directives.unchanged,
    }

    def run(self):
        """Process .bib files, set file dependencies, and create a
        node that is to be transformed to the entries of the
        bibliography.
        """
        env = cast(BuildEnvironment, self.state.document.settings.env)
        domain = cast(BibtexDomain, env.get_domain('cite'))
        if "filter" in self.options:
            if "all" in self.options:
                logger.warning(":filter: overrides :all:")
            if "notcited" in self.options:
                logger.warning(":filter: overrides :notcited:")
            if "cited" in self.options:
                logger.warning(":filter: overrides :cited:")
            try:
                filter_ = ast.parse(self.options["filter"])
            except SyntaxError:
                logger.warning(
                    "syntax error in :filter: expression" +
                    " (" + self.options["filter"] + "); "
                    "the option will be ignored"
                )
                filter_ = ast.parse("cited")
        elif "all" in self.options:
            filter_ = ast.parse("True")
        elif "notcited" in self.options:
            filter_ = ast.parse("not cited")
        else:
            # the default filter: include only cited entries
            filter_ = ast.parse("cited")
        if self.arguments:
            bibfiles = []
            for bibfile in self.arguments[0].split():
                normbibfile = normpath_filename(env, bibfile)
                if normbibfile not in domain.bibfiles:
                    logger.warning(
                        "{0} not found or not configured"
                        " in bibtex_bibfiles".format(bibfile),
                        location=(env.docname, self.lineno))
                else:
                    bibfiles.append(normbibfile)
        else:
            bibfiles = list(domain.bibfiles.keys())
        for bibfile in bibfiles:
            env.note_dependency(bibfile)
        # generate nodes and ids
        keyprefix = self.options.get("keyprefix", "")
        list_ = self.options.get("list", "citation")
        if list_ not in {"bullet", "enumerated", "citation"}:
            logger.warning(
                "unknown bibliography list type '{0}'.".format(list_))
            list_ = "citation"
        if list_ in {"bullet", "enumerated"}:
            citation_node_class = docutils.nodes.list_item
        else:
            citation_node_class = docutils.nodes.citation
        node = bibliography_node('', docname=env.docname)
        self.state.document.note_explicit_target(node, node)
        # we only know which citations to included at resolve stage
        # but we need to know their ids before resolve stage
        # so for now we generate a node, and thus, an id, for every entry
        citation_nodes = {keyprefix + entry.key: citation_node_class()
                          for entry in domain.get_entries(bibfiles)}
        for citation_node in citation_nodes.values():
            self.state.document.note_explicit_target(
                citation_node, citation_node)
        # create bibliography object
        bibliography = BibliographyValue(
            line=self.lineno,
            list_=list_,
            enumtype=self.options.get("enumtype", "arabic"),
            start=self.options.get("start", 1),
            style=self.options.get(
                "style", env.app.config.bibtex_default_style),
            filter_=filter_,
            labelprefix=self.options.get("labelprefix", ""),
            keyprefix=keyprefix,
            bibfiles=bibfiles,
            citation_nodes=citation_nodes
        )
        bib_key = BibliographyKey(docname=env.docname, id_=node['ids'][0])
        assert bib_key not in domain.bibliographies
        domain.bibliographies[bib_key] = bibliography
        return [node]
