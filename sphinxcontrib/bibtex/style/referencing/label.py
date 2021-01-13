import dataclasses

from typing import TYPE_CHECKING, List, Iterable
from pybtex.style.template import words
from sphinxcontrib.bibtex.style.template import reference, entry_label, join
from sphinxcontrib.bibtex.richtext import ReferenceInfo
from . import BaseStandardReferenceStyle, BaseNamesReferenceStyle

if TYPE_CHECKING:
    from pybtex.richtext import BaseText
    from pybtex.style.template import Node


@dataclasses.dataclass(frozen=True)
class LabelReferenceStyle(
        BaseStandardReferenceStyle[ReferenceInfo],
        BaseNamesReferenceStyle[ReferenceInfo]):
    """Reference by label if parenthetical,
    and by author and label if textual.
    """

    def get_role_names(self) -> Iterable[str]:
        return [
            f'{capfirst}{parenthetical}{full_author}'
            for parenthetical in ['p', 't']
            for capfirst in ['', 'c']
            for full_author in ['', 's']
        ]

    def get_outer_template(
            self, role_name: str, children: List["BaseText"]) -> "Node":
        if 'p' in role_name:  # parenthetical
            return self.get_standard_outer_template(
                children,
                brackets=True,
                capfirst=False)
        else:  # textual
            return self.get_standard_outer_template(
                children,
                brackets=False,
                capfirst='c' in role_name)

    def get_inner_template(self, role_name: str) -> "Node":
        if 'p' in role_name:  # parenthetical
            return reference[entry_label]
        else:  # textual
            return words[
                self.get_author_template(full_authors='s' in role_name),
                join[
                    self.left_bracket,
                    reference[entry_label],
                    self.right_bracket
                ]
            ]
