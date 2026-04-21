"""
Domain for footnote citations.

.. autoclass:: BibtexFootDomain
    :members:
"""

from collections.abc import Sequence
from typing import TYPE_CHECKING, AbstractSet, Any, Dict, List, Tuple

import docutils.nodes
import docutils.utils
import sphinx.util
from sphinx.domains import Domain, ObjType
from sphinx.locale import _

from .foot_roles import FootCiteRole
from .style.referencing import BaseReferenceStyle

if TYPE_CHECKING:
    from sphinx.addnodes import pending_xref
    from sphinx.builders import Builder
    from sphinx.environment import BuildEnvironment

logger = sphinx.util.logging.getLogger(__name__)


class BibtexFootDomain(Domain):
    """Sphinx domain for footnote citations."""

    name = "footcite"
    label = "BibTeX Footnote Citations"
    data_version = 0
    reference_style: BaseReferenceStyle
    _role_names: Sequence[str] = [
        "p",
        "ps",
        "t",
        "ts",
        "ct",
        "cts",
    ]
    object_types = {"citation": ObjType(_("citation"), *_role_names, searchprio=-1)}
    roles = {role_name: FootCiteRole() for role_name in _role_names}

    def merge_domaindata(
        self, docnames: AbstractSet[str], otherdata: Dict[str, Any]
    ) -> None:
        """Merge in data regarding *docnames* from domain data
        inventory *otherdata*.

        As there is no document specific data for this domain, this function
        does nothing.
        """
        pass

    def resolve_any_xref(
        self,
        env: "BuildEnvironment",
        fromdocname: str,
        builder: "Builder",
        target: str,
        node: "pending_xref",
        contnode: docutils.nodes.Element,
    ) -> List[Tuple[str, docutils.nodes.reference]]:
        """Resolve the pending reference *node* with the given *target*,
        where the reference comes from an "any" role.

        Since citation references are resolved to regular citations,
        and not to footnote citations,
        this implementation simply returns an empty list.
        """
        return []
