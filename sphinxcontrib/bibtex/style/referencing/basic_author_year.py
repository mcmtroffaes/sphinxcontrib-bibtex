import dataclasses
from typing import TYPE_CHECKING, List, Iterable, Union
from sphinxcontrib.bibtex.style.template import reference, join
from pybtex.style.template import words, field
from . import BaseReferenceStyle, BracketStyle, PersonStyle

if TYPE_CHECKING:
    from pybtex.richtext import BaseText
    from pybtex.style.template import Node


@dataclasses.dataclass
class BasicAuthorYearReferenceStyle(BaseReferenceStyle):
    """Textual or parenthetical reference by author-year."""

    #: Bracket style.
    bracket: BracketStyle = BracketStyle()

    #: Person style.
    person: PersonStyle = PersonStyle()

    #: Separator between author and year for textual citations.
    author_year_sep: Union["BaseText", str] = ', '

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
            return reference[
                join(sep=self.author_year_sep)[
                    self.person.names(
                        'author', full='s' in role_name),
                    field('year')
                ]
            ]
        else:  # textual
            return words[
                self.person.names('author', full='s' in role_name),
                join[
                    self.bracket.left,
                    reference[field('year')],
                    self.bracket.right
                ]
            ]
