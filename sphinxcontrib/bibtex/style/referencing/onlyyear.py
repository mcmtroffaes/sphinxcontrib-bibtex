from typing import TYPE_CHECKING, List, Iterable

from pybtex.style.template import field
from . import BaseStandardReferenceStyle, reference


if TYPE_CHECKING:
    from pybtex.richtext import BaseText
    from pybtex.style.template import Node


class OnlyYearReferenceStyle(BaseStandardReferenceStyle):
    """Reference by year."""

    def get_role_names(self) -> Iterable[str]:
        return ['year', 'yearpar']

    def get_outer_template(
            self, role_name: str, children: List["BaseText"]) -> "Node":
        return self.get_standard_outer_template(
            children,
            brackets='par' in role_name,
            capfirst=False,
        )

    def get_inner_template(self, role_name: str) -> "Node":
        return reference[field('year')]