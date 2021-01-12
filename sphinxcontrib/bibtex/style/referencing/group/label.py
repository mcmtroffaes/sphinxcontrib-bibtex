import dataclasses

from . import BaseGroupReferenceStyle
from .. import ReferenceInfo, BaseStandardReferenceStyle
from ..label import LabelReferenceStyle
from ..onlyauthor import OnlyAuthorReferenceStyle
from ..onlylabel import OnlyLabelReferenceStyle
from ..onlyyear import OnlyYearReferenceStyle


@dataclasses.dataclass(frozen=True)
class LabelGroupReferenceStyle(
        BaseGroupReferenceStyle[ReferenceInfo],
        BaseStandardReferenceStyle[ReferenceInfo]):

    def __post_init__(self):
        self.styles.extend([
            LabelReferenceStyle(
                ReferenceText=self.ReferenceText,
                name_style=self.name_style,
                abbreviate_names=self.abbreviate_names,
                left_bracket=self.left_bracket,
                right_bracket=self.right_bracket,
                outer_separators=self.outer_separators,
                names_separators=self.names_separators,
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
