"""
    .. autoclass:: bibliography
"""

from docutils import nodes
from docutils.nodes import SkipNode
from sphinx.writers.latex import LaTeXTranslator


class bibliography(nodes.General, nodes.Element):
    """Node for representing a bibliography. Replaced by a list of
    citations by
    :class:`~sphinxcontrib.bibtex.transforms.BibliographyTransform`.
    """
    pass


class raw_latex(
        nodes.Special, nodes.Inline, nodes.PreBibliographic,
        nodes.FixedTextElement):
    """Node for representing raw latex data."""
    pass


def visit_raw_latex(self: LaTeXTranslator, node: raw_latex):
    self.body.append(node.rawsource)
    raise SkipNode


def depart_raw_latex(self: LaTeXTranslator, node: raw_latex):
    pass
