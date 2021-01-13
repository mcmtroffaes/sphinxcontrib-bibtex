import dataclasses

from sphinxcontrib.bibtex.style.referencing import (
    ReferenceInfo, BaseStandardReferenceStyle, BaseNamesReferenceStyle,
    BaseGroupReferenceStyle
)
from .basic_numbers import BasicNumbersReferenceStyle
from .basic_author import BasicAuthorReferenceStyle
from .basic_label import BasicLabelReferenceStyle
from .basic_year import BasicYearReferenceStyle


@dataclasses.dataclass(frozen=True)
class NumbersReferenceStyle(
        BaseGroupReferenceStyle[ReferenceInfo],
        BaseNamesReferenceStyle[ReferenceInfo],
        BaseStandardReferenceStyle[ReferenceInfo],
):

    def __post_init__(self):
        self.styles.extend([
            BasicNumbersReferenceStyle(
                ReferenceText=self.ReferenceText,
                name_style_plugin=self.name_style_plugin,
                abbreviate_names=self.abbreviate_names,
                left_bracket=self.left_bracket,
                right_bracket=self.right_bracket,
                outer_separators=self.outer_separators,
                names_separators=self.names_separators,
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
