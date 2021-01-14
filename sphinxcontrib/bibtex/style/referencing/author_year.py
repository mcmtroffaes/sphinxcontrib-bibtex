import dataclasses
from typing import Union, TYPE_CHECKING

from sphinxcontrib.bibtex.style.referencing import (
    ReferenceInfo, BaseBracketReferenceStyle, BaseNamesReferenceStyle,
    BaseGroupReferenceStyle
)
from .basic_author_year import BasicAuthorYearReferenceStyle
from .extra_author import ExtraAuthorReferenceStyle
from .extra_label import ExtraLabelReferenceStyle
from .extra_year import ExtraYearReferenceStyle

if TYPE_CHECKING:
    from pybtex.richtext import BaseText


@dataclasses.dataclass(frozen=True)
class AuthorYearReferenceStyle(
        BaseBracketReferenceStyle[ReferenceInfo],
        BaseNamesReferenceStyle[ReferenceInfo],
        BaseGroupReferenceStyle[ReferenceInfo]):
    """Textual or parenthetical reference by author-year,
    or just by author, label, or year.
    """

    #: Separator between author and year for textual citations.
    author_year_sep: Union["BaseText", str] = ', '

    def __post_init__(self):
        self.styles.extend([
            BasicAuthorYearReferenceStyle(
                ReferenceText=self.ReferenceText,
                left_bracket=self.left_bracket,
                right_bracket=self.right_bracket,
                outer_sep=self.outer_sep,
                outer_sep2=self.outer_sep2,
                outer_last_sep=self.outer_last_sep,
                name_style=self.name_style,
                abbreviate_names=self.abbreviate_names,
                names_sep=self.names_sep,
                names_sep2=self.names_sep2,
                names_last_sep=self.names_last_sep,
                names_other=self.names_other,
                author_year_sep=self.author_year_sep,
            ),
            ExtraAuthorReferenceStyle(
                ReferenceText=self.ReferenceText,
                left_bracket=self.left_bracket,
                right_bracket=self.right_bracket,
                outer_sep=self.outer_sep,
                outer_sep2=self.outer_sep2,
                outer_last_sep=self.outer_last_sep,
                name_style=self.name_style,
                abbreviate_names=self.abbreviate_names,
                names_sep=self.names_sep,
                names_sep2=self.names_sep2,
                names_last_sep=self.names_last_sep,
                names_other=self.names_other,
            ),
            ExtraLabelReferenceStyle(
                ReferenceText=self.ReferenceText,
                left_bracket=self.left_bracket,
                right_bracket=self.right_bracket,
                outer_sep=self.outer_sep,
                outer_sep2=self.outer_sep2,
                outer_last_sep=self.outer_last_sep,
            ),
            ExtraYearReferenceStyle(
                ReferenceText=self.ReferenceText,
                left_bracket=self.left_bracket,
                right_bracket=self.right_bracket,
                outer_sep=self.outer_sep,
                outer_sep2=self.outer_sep2,
                outer_last_sep=self.outer_last_sep,
            )
        ])
        super().__post_init__()
