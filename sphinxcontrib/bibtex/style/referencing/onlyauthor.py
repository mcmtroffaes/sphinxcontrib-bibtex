import dataclasses

from typing import TYPE_CHECKING, List, Iterable
from . import (
    ReferenceInfo, BaseStandardReferenceStyle, BaseNamesReferenceStyle,
    reference
)


if TYPE_CHECKING:
    from pybtex.richtext import BaseText
    from pybtex.style.template import Node


@dataclasses.dataclass(frozen=True)
class OnlyAuthorReferenceStyle(
        BaseStandardReferenceStyle[ReferenceInfo],
        BaseNamesReferenceStyle[ReferenceInfo]):
    """Reference by author names."""

    def get_role_names(self) -> Iterable[str]:
        return [
            f'{capfirst}author{parenthetical}{full_author}'
            for parenthetical in ['par', '']
            for capfirst in ['', 'c']
            for full_author in ['', 's']
        ]

    def get_outer_template(
            self, role_name: str, children: List["BaseText"]) -> "Node":
        return self.get_standard_outer_template(
            children,
            brackets='par' in role_name,
            capfirst='c' in role_name,
        )

    def get_inner_template(self, role_name: str) -> "Node":
        return reference[
            self.get_author_template(full_authors='s' in role_name)]
