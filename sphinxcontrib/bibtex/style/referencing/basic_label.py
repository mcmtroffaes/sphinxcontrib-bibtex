import dataclasses

from typing import TYPE_CHECKING, List, Iterable
from pybtex.style.template import words
from sphinxcontrib.bibtex.style.template import reference, entry_label, join
from . import BracketStyle, PersonStyle, BaseReferenceStyle

if TYPE_CHECKING:
    from pybtex.richtext import BaseText
    from pybtex.style.template import Node


@dataclasses.dataclass
class BasicLabelReferenceStyle(BaseReferenceStyle):
    """Reference by label if parenthetical,
    and by author and label if textual.
    """

    bracket: BracketStyle = BracketStyle()
    person: PersonStyle = PersonStyle()

    def get_role_names(self) -> Iterable[str]:
        return [
            f'{capfirst}{parenthetical}{full_author}'
            for parenthetical in ['p', 't']
            for capfirst in (['', 'c'] if parenthetical == 't' else [''])
            for full_author in ['', 's']
        ]

    def get_outer(
            self, role_name: str, children: List["BaseText"]) -> "Node":
        if 'p' in role_name:  # parenthetical
            return self.bracket.get_outer(
                children,
                brackets=True,
                capfirst=False)
        else:  # textual
            return self.bracket.get_outer(
                children,
                brackets=False,
                capfirst='c' in role_name)

    def get_inner(self, role_name: str) -> "Node":
        if 'p' in role_name:  # parenthetical
            return reference[entry_label]
        else:  # textual
            return words[
                self.person.names('author', full='s' in role_name),
                join[
                    self.bracket.left,
                    reference[entry_label],
                    self.bracket.right
                ]
            ]
