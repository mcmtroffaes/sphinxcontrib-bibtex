import dataclasses
from typing import Union, TYPE_CHECKING

from sphinxcontrib.bibtex.style.referencing import (
    ReferenceInfo, BaseStandardReferenceStyle, BaseNamesReferenceStyle,
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
            ExtraAuthorReferenceStyle(
                ReferenceText=self.ReferenceText,
                name_style_plugin=self.name_style_plugin,
                abbreviate_names=self.abbreviate_names,
                left_bracket=self.left_bracket,
                right_bracket=self.right_bracket,
                outer_separators=self.outer_separators,
                names_separators=self.names_separators,
            ),
            ExtraLabelReferenceStyle(
                ReferenceText=self.ReferenceText,
                left_bracket=self.left_bracket,
                right_bracket=self.right_bracket,
                outer_separators=self.outer_separators,
            ),
            ExtraYearReferenceStyle(
                ReferenceText=self.ReferenceText,
                left_bracket=self.left_bracket,
                right_bracket=self.right_bracket,
                outer_separators=self.outer_separators,
            )
        ])
        super().__post_init__()
