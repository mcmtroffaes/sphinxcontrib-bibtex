"""
    New Doctree Nodes
    ~~~~~~~~~~~~~~~~~

    .. autoclass:: bibliography
"""

from docutils import nodes


class bibliography(nodes.General, nodes.Element):
    """Node for representing a bibliography. Replaced by a list of
    citations by
    :class:`~sphinxcontrib.bibtex.transforms.BibliographyTransform`.
    """
    pass


class fnbibliography(nodes.General, nodes.Element):
    """Node for representing a footnote bibliography. Replaced by a list
    of footnotes by
    :class:`~sphinxcontrib.bibtex.transforms.BibliographyTransform`.
    """
    pass
