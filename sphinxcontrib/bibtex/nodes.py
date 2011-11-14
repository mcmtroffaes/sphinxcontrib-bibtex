"""
    New Doctree Nodes
    ~~~~~~~~~~~~~~~~~

    .. autoclass:: bibliography
    .. autoclass:: cite
"""

from docutils import nodes

class bibliography(nodes.General, nodes.Element):
    """Node for representing a bibliography. Replaced by a list of
    citations or footnotes (depending on the style) on
    doctree-resolved.
    """
    pass

class cite(nodes.General, nodes.TextElement):
    """Node for representing a citation with the :rst:role:`cite`
    role.
    """
    pass
