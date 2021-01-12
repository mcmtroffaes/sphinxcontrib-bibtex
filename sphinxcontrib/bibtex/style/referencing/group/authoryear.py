import dataclasses

from . import BaseGroupReferenceStyle
from .. import ReferenceInfo, BaseStandardReferenceStyle
from ..authoryear import AuthorYearReferenceStyle
from ..onlyauthor import OnlyAuthorReferenceStyle
from ..onlylabel import OnlyLabelReferenceStyle
from ..onlyyear import OnlyYearReferenceStyle


@dataclasses.dataclass(frozen=True)
class AuthorYearGroupReferenceStyle(
        BaseGroupReferenceStyle[ReferenceInfo],
        BaseStandardReferenceStyle[ReferenceInfo]):

    author_year_sep: str

    def __post_init__(self):
        self.styles.extend([
            AuthorYearReferenceStyle(
                ReferenceText=self.ReferenceText,
                name_style=self.name_style,
                abbreviate_names=self.abbreviate_names,
                left_bracket=self.left_bracket,
                right_bracket=self.right_bracket,
                outer_separators=self.outer_separators,
                names_separators=self.names_separators,
                author_year_sep=self.author_year_sep,
            ),
            OnlyAuthorReferenceStyle(
                ReferenceText=self.ReferenceText,
                name_style=self.name_style,
                abbreviate_names=self.abbreviate_names,
                left_bracket=self.left_bracket,
                right_bracket=self.right_bracket,
                outer_separators=self.outer_separators,
                names_separators=self.names_separators,
            ),
            OnlyLabelReferenceStyle(
                ReferenceText=self.ReferenceText,
                name_style=self.name_style,
                abbreviate_names=self.abbreviate_names,
                left_bracket=self.left_bracket,
                right_bracket=self.right_bracket,
                outer_separators=self.outer_separators,
                names_separators=self.names_separators,
            ),
            OnlyYearReferenceStyle(
                ReferenceText=self.ReferenceText,
                name_style=self.name_style,
                abbreviate_names=self.abbreviate_names,
                left_bracket=self.left_bracket,
                right_bracket=self.right_bracket,
                outer_separators=self.outer_separators,
                names_separators=self.names_separators,
            )
        ])
        super().__post_init__()
