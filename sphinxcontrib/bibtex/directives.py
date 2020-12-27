"""
    .. autoclass:: BibliographyDirective

        .. automethod:: run

    .. autofunction:: process_start_option
"""

import ast  # parse(), used for filter
import sphinx.util

from typing import cast
from docutils.parsers.rst import Directive, directives
from sphinx.environment import BuildEnvironment
from sphinx.util.console import standout

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
                logger.warning(standout(":filter: overrides :all:"))
            if "notcited" in self.options:
                logger.warning(standout(":filter: overrides :notcited:"))
            if "cited" in self.options:
                logger.warning(standout(":filter: overrides :cited:"))
            try:
                filter_ = ast.parse(self.options["filter"])
            except SyntaxError:
                logger.warning(
                    standout("syntax error in :filter: expression") +
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
            bibfiles = [normpath_filename(env, bibfile)
                        for bibfile in self.arguments[0].split()]
        else:
            bibfiles = list(domain.bibfiles.keys())
        bibliography = BibliographyValue(
            line=self.lineno,
            list_=self.options.get("list", "citation"),
            enumtype=self.options.get("enumtype", "arabic"),
            start=self.options.get("start", 1),
            style=self.options.get(
                "style", env.app.config.bibtex_default_style),
            filter_=filter_,
            labelprefix=self.options.get("labelprefix", ""),
            keyprefix=self.options.get("keyprefix", ""),
            bibfiles=bibfiles,
        )
        if bibliography.list_ not in {"bullet", "enumerated", "citation"}:
            logger.warning("unknown bibliography list type '{0}'.".format(
                bibliography.list_))
        for bibfile in bibfiles:
            env.note_dependency(bibfile)
        node = bibliography_node('')
        self.state.document.note_explicit_target(node)
        bib_key = BibliographyKey(docname=env.docname, id_=node['ids'][0])
        assert bib_key not in domain.bibliographies
        domain.bibliographies[bib_key] = bibliography
        return [node]
