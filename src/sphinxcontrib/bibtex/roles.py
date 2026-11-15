"""
.. autoclass:: CitationRef
    :members:

.. autoclass:: CiteRole
    :show-inheritance:

    .. automethod:: result_nodes
"""

from typing import TYPE_CHECKING, List, NamedTuple, Tuple, cast

import docutils.nodes
from pybtex.plugin import find_plugin
from sphinx.addnodes import only, pending_xref
from sphinx.roles import XRefRole

from .citation_target import CitationTarget, parse_citation_targets

if TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx.util.tags import Tags

    from .domain import BibtexDomain


class CitationRef(NamedTuple):
    """Information about a citation reference."""

    citation_ref_id: str  #: Unique id of this citation reference.
    docname: str  #: Document name.
    line: int  #: Line number.
    targets: List[CitationTarget]  #: Citation targets (key, pre, post).
    only_conditions: Tuple[str, ...] = ()  #: Enclosing only expressions.


def is_active_only(conditions: Tuple[str, ...], tags: "Tags") -> bool:
    """Whether all enclosing only expressions keep their children."""
    for condition in conditions:
        try:
            if not tags.eval_condition(condition):
                return False
        except Exception:
            # Sphinx keeps the children on an invalid expression and emits
            # its own warning when processing the only node later.
            continue
    return True


def process_citation_refs(app: "Sphinx", doctree: docutils.nodes.document) -> None:
    """Record only conditions once the citation nodes have their parents."""
    conditions = {}
    for node in doctree.findall(pending_xref):
        if node.get("refdomain") != "cite":
            continue
        expressions = []
        parent = node.parent
        while parent is not None:
            if isinstance(parent, only):
                expressions.append(parent["expr"])
            parent = parent.parent
        node["bibtex_only_conditions"] = tuple(expressions)
        conditions[node["ids"][0]] = tuple(expressions)
    domain = cast("BibtexDomain", app.env.get_domain("cite"))
    domain.data["citation_refs"] = [
        ref._replace(only_conditions=conditions[ref.citation_ref_id])
        if ref.docname == app.env.docname and ref.citation_ref_id in conditions
        else ref
        for ref in domain.citation_refs
    ]


class CiteRole(XRefRole):
    """Class for processing the :rst:role:`cite` role."""

    backend = find_plugin("pybtex.backends", "docutils")()
    innernodeclass = docutils.nodes.inline

    def result_nodes(self, document, env, node, is_ref):
        """Associate the pending_xref with the cite domain,
        and note the cited citation keys.
        """
        if not node.get("refdomain"):
            assert node["reftype"] == "cite"
            node["refdomain"] = "cite"
            node["reftype"] = "p"
        document.note_explicit_target(node, node)  # for backrefs
        domain = cast("BibtexDomain", env.get_domain("cite"))
        domain.citation_refs.append(
            CitationRef(
                citation_ref_id=node["ids"][0],
                docname=env.docname,
                line=document.line,
                targets=list(parse_citation_targets(self.target)),
            )
        )
        return [node], []
