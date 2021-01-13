import dataclasses
from typing import Union, TYPE_CHECKING

from sphinxcontrib.bibtex.style.referencing import (
    ReferenceInfo, BaseStandardReferenceStyle, BaseNamesReferenceStyle,
    BaseGroupReferenceStyle
)
from .basic_author_year import BasicAuthorYearReferenceStyle
from .basic_author import BasicAuthorReferenceStyle
from .basic_label import BasicLabelReferenceStyle
from .basic_year import BasicYearReferenceStyle

if TYPE_CHECKING:
    from pybtex.richtext import BaseText


@dataclasses.dataclass(frozen=True)
class AuthorYearReferenceStyle(
        BaseGroupReferenceStyle[ReferenceInfo],
        BaseNamesReferenceStyle[ReferenceInfo],
        BaseStandardReferenceStyle[ReferenceInfo]):

    author_year_sep: Union["BaseText", str] = ', '

    def __post_init__(self):
        self.styles.extend([
            BasicAuthorYearReferenceStyle(
                ReferenceText=self.ReferenceText,
                name_style_plugin=self.name_style_plugin,
                abbreviate_names=self.abbreviate_names,
                left_bracket=self.left_bracket,
                right_bracket=self.right_bracket,
                outer_separators=self.outer_separators,
                names_separators=self.names_separators,
                author_year_sep=self.author_year_sep,
            ),
            BasicAuthorReferenceStyle(
                ReferenceText=self.ReferenceText,
                name_style_plugin=self.name_style_plugin,
                abbreviate_names=self.abbreviate_names,
                left_bracket=self.left_bracket,
                right_bracket=self.right_bracket,
                outer_separators=self.outer_separators,
                names_separators=self.names_separators,
            ),
            BasicLabelReferenceStyle(
                ReferenceText=self.ReferenceText,
                left_bracket=self.left_bracket,
                right_bracket=self.right_bracket,
                outer_separators=self.outer_separators,
            ),
            BasicYearReferenceStyle(
                ReferenceText=self.ReferenceText,
                left_bracket=self.left_bracket,
                right_bracket=self.right_bracket,
                outer_separators=self.outer_separators,
            )
        ])
        super().__post_init__()
