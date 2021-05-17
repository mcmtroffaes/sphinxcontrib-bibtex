import dataclasses

from sphinxcontrib.bibtex.style.template import reference
from typing import TYPE_CHECKING, List, Iterable
from . import BracketStyle, PersonStyle, BaseReferenceStyle


if TYPE_CHECKING:
    from pybtex.richtext import BaseText
    from pybtex.style.template import Node


@dataclasses.dataclass
class ExtraAuthorReferenceStyle(BaseReferenceStyle):
    """Reference just by author names."""

    #: Bracket style.
    bracket: BracketStyle = BracketStyle()

    #: Person style.
    person: PersonStyle = PersonStyle()

    def role_names(self) -> Iterable[str]:
        return [
            f'{capfirst}author{parenthetical}{full_author}'
            for parenthetical in ['par', '']
            for capfirst in (['', 'c'] if parenthetical == '' else [''])
            for full_author in ['', 's']
        ]

    def outer(self, role_name: str, children: List["BaseText"]) -> "Node":
        return self.bracket.outer(
            children,
            brackets='par' in role_name,
            capfirst='c' in role_name,
        )

    def inner(self, role_name: str) -> "Node":
        return reference[
            self.person.names('author', full='s' in role_name)]
