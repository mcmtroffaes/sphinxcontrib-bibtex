import dataclasses
from typing import TYPE_CHECKING, List, Iterable, Union
from sphinxcontrib.bibtex.style.template import reference, join
from pybtex.style.template import words, field
from . import BaseReferenceStyle, BracketStyle, PersonStyle

if TYPE_CHECKING:
    from pybtex.richtext import BaseText
    from pybtex.style.template import Node


@dataclasses.dataclass
class BasicAuthorYearParentheticalReferenceStyle(BaseReferenceStyle):
    """Parenthetical reference by author-year."""

    #: Bracket style.
    bracket: BracketStyle = BracketStyle()

    #: Person style.
    person: PersonStyle = PersonStyle()

    #: Separator between author and year.
    author_year_sep: Union["BaseText", str] = ', '

    def role_names(self) -> Iterable[str]:
        return [f'p{full_author}' for full_author in ['', 's']]

    def outer(self, role_name: str, children: List["BaseText"]) -> "Node":
        return self.bracket.outer(
            children,
            brackets=True,
            capfirst=False)

    def inner(self, role_name: str) -> "Node":
        return reference[
            join(sep=self.author_year_sep)[
                self.person.names(
                    'author', full='s' in role_name),
                field('year')
            ]
        ]


@dataclasses.dataclass
class BasicAuthorYearTextualReferenceStyle(BaseReferenceStyle):
    """Textual reference by author-year."""

    #: Bracket style.
    bracket: BracketStyle = BracketStyle()

    #: Person style.
    person: PersonStyle = PersonStyle()

    def role_names(self) -> Iterable[str]:
        return [f'{capfirst}t{full_author}'
                for capfirst in ['', 'c'] for full_author in ['', 's']]

    def outer(self, role_name: str, children: List["BaseText"]) -> "Node":
        return self.bracket.outer(
            children,
            brackets=False,
            capfirst='c' in role_name)

    def inner(self, role_name: str) -> "Node":
        return words[
            self.person.names('author', full='s' in role_name),
            join[
                self.bracket.left,
                reference[field('year')],
                self.bracket.right
            ]
        ]
