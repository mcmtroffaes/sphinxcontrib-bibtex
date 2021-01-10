from typing import TYPE_CHECKING, List
from pybtex.style.template import words
from . import (
    BaseReferenceStyle,
    reference, entry_label, join, Role,
)


if TYPE_CHECKING:
    from pybtex.richtext import BaseText
    from pybtex.style.template import Node


class LabelReferenceStyle(BaseReferenceStyle):
    """Simple parenthetical references by label."""

    def get_parenthetical_outer_template(
            self, role: Role, children: List["BaseText"]) -> "Node":
        return self.get_outer_template_helper(
            children,
            separators=self.outer_separators[role.type_],
            brackets=role.brackets,
            capfirst=False)

    def get_parenthetical_inner_template(self, role: Role) -> "Node":
        return reference[entry_label]

    def get_textual_outer_template(
            self, role: Role, children: List["BaseText"]) -> "Node":
        return self.get_outer_template_helper(
            children,
            separators=self.outer_separators[role.type_],
            brackets=False,
            capfirst=role.capfirst)

    def get_textual_inner_template(self, role: Role) -> "Node":
        return words[
            self.get_names_template_helper(role.full_authors),
            join[
                self.left_bracket if role.brackets else '',
                reference[entry_label],
                self.right_bracket if role.brackets else ''
            ]
        ]
