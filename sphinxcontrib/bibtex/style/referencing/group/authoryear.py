import dataclasses

from . import GroupReferenceStyle
from .. import ReferenceInfo, BaseStandardReferenceStyle
from ..authoronly import AuthorOnlyReferenceStyle
from ..authoryear import AuthorYearReferenceStyle
from ..labelonly import LabelOnlyReferenceStyle
from ..yearonly import YearOnlyReferenceStyle


@dataclasses.dataclass(frozen=True)
class AuthorYearGroupReferenceStyle(
        GroupReferenceStyle[ReferenceInfo],
        BaseStandardReferenceStyle[ReferenceInfo]):

    def __post_init__(self):
        self.styles += [
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
            AuthorOnlyReferenceStyle(
                ReferenceText=self.ReferenceText,
                name_style=self.name_style,
                abbreviate_names=self.abbreviate_names,
                left_bracket=self.left_bracket,
                right_bracket=self.right_bracket,
                outer_separators=self.outer_separators,
                names_separators=self.names_separators,
            ),
            LabelOnlyReferenceStyle(
                ReferenceText=self.ReferenceText,
                name_style=self.name_style,
                abbreviate_names=self.abbreviate_names,
                left_bracket=self.left_bracket,
                right_bracket=self.right_bracket,
                outer_separators=self.outer_separators,
                names_separators=self.names_separators,
            ),
            YearOnlyReferenceStyle(
                ReferenceText=self.ReferenceText,
                name_style=self.name_style,
                abbreviate_names=self.abbreviate_names,
                left_bracket=self.left_bracket,
                right_bracket=self.right_bracket,
                outer_separators=self.outer_separators,
                names_separators=self.names_separators,
            )
        ]
        super().__post_init__()
