import dataclasses
from typing import Union, TYPE_CHECKING

from sphinxcontrib.bibtex.style.referencing import (
    BracketStyle, PersonStyle, GroupReferenceStyle
)
from .basic_author_year import BasicAuthorYearReferenceStyle
from .extra_author import ExtraAuthorReferenceStyle
from .extra_label import ExtraLabelReferenceStyle
from .extra_year import ExtraYearReferenceStyle

if TYPE_CHECKING:
    from pybtex.richtext import BaseText


@dataclasses.dataclass
class AuthorYearReferenceStyle(GroupReferenceStyle):
    """Textual or parenthetical reference by author-year,
    or just by author, label, or year.
    """

    #: Bracket style.
    bracket: BracketStyle = BracketStyle()

    #: Person style.
    person: PersonStyle = PersonStyle()

    #: Separator between author and year for textual citations.
    author_year_sep: Union["BaseText", str] = ', '

    def __post_init__(self):
        self.styles.extend([
            BasicAuthorYearReferenceStyle(
                bracket=self.bracket,
                person=self.person,
                author_year_sep=self.author_year_sep,
            ),
            ExtraAuthorReferenceStyle(
                bracket=self.bracket,
                person=self.person,
            ),
            ExtraLabelReferenceStyle(
                bracket=self.bracket,
            ),
            ExtraYearReferenceStyle(
                bracket=self.bracket,
            )
        ])
        super().__post_init__()
