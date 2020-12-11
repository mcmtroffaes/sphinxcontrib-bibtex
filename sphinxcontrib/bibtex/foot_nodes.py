"""
    .. autoclass:: footbibliography
"""

from docutils import nodes


class footbibliography(nodes.General, nodes.Element):
    """Node for representing a bibliography. Replaced by a list of
    citations by
    :class:`~sphinxcontrib.bibtex.foot_transforms.FootBibliographyTransform`.
    """
    pass
