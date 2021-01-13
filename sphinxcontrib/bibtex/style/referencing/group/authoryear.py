import dataclasses
from typing import Union, TYPE_CHECKING

from .. import (
    ReferenceInfo, BaseStandardReferenceStyle, BaseNamesReferenceStyle,
    BaseGroupReferenceStyle
)
from ..authoryear import AuthorYearReferenceStyle
from ..onlyauthor import OnlyAuthorReferenceStyle
from ..onlylabel import OnlyLabelReferenceStyle
from ..onlyyear import OnlyYearReferenceStyle

if TYPE_CHECKING:
    from pybtex.richtext import BaseText


@dataclasses.dataclass(frozen=True)
class AuthorYearGroupReferenceStyle(
        BaseGroupReferenceStyle[ReferenceInfo],
        BaseNamesReferenceStyle[ReferenceInfo],
        BaseStandardReferenceStyle[ReferenceInfo]):

    author_year_sep: Union["BaseText", str] = ', '

    def __post_init__(self):
        self.styles.extend([
            AuthorYearReferenceStyle(
                ReferenceText=self.ReferenceText,
                name_style_plugin=self.name_style_plugin,
                abbreviate_names=self.abbreviate_names,
                left_bracket=self.left_bracket,
                right_bracket=self.right_bracket,
                outer_separators=self.outer_separators,
                names_separators=self.names_separators,
                author_year_sep=self.author_year_sep,
            ),
            OnlyAuthorReferenceStyle(
                ReferenceText=self.ReferenceText,
                name_style_plugin=self.name_style_plugin,
                abbreviate_names=self.abbreviate_names,
                left_bracket=self.left_bracket,
                right_bracket=self.right_bracket,
                outer_separators=self.outer_separators,
                names_separators=self.names_separators,
            ),
            OnlyLabelReferenceStyle(
                ReferenceText=self.ReferenceText,
                left_bracket=self.left_bracket,
                right_bracket=self.right_bracket,
                outer_separators=self.outer_separators,
            ),
            OnlyYearReferenceStyle(
                ReferenceText=self.ReferenceText,
                left_bracket=self.left_bracket,
                right_bracket=self.right_bracket,
                outer_separators=self.outer_separators,
            )
        ])
        super().__post_init__()
