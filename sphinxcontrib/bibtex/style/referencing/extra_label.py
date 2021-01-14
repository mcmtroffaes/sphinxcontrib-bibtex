import dataclasses

from sphinxcontrib.bibtex.style.template import reference, entry_label
from sphinxcontrib.bibtex.richtext import ReferenceInfo
from typing import TYPE_CHECKING, List, Iterable
from . import BracketReferenceStyleMixin

if TYPE_CHECKING:
    from pybtex.richtext import BaseText
    from pybtex.style.template import Node


@dataclasses.dataclass
class ExtraLabelReferenceStyle(BracketReferenceStyleMixin[ReferenceInfo]):
    """Reference just by label."""

    def get_role_names(self) -> Iterable[str]:
        return ['label', 'labelpar']

    def get_outer_template(
            self, role_name: str, children: List["BaseText"]) -> "Node":
        return self.get_bracket_outer_template(
            children,
            brackets='par' in role_name,
            capfirst=False,
        )

    def get_inner_template(self, role_name: str) -> "Node":
        return reference[entry_label]
