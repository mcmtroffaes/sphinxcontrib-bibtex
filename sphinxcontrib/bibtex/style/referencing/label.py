import dataclasses

from sphinxcontrib.bibtex.style.referencing import (
    ReferenceInfo, BaseBracketReferenceStyle, BaseNamesReferenceStyle,
    BaseGroupReferenceStyle
)
from .basic_label import BasicLabelReferenceStyle
from .extra_author import ExtraAuthorReferenceStyle
from .extra_label import ExtraLabelReferenceStyle
from .extra_year import ExtraYearReferenceStyle


@dataclasses.dataclass(frozen=True)
class LabelReferenceStyle(
        BaseGroupReferenceStyle[ReferenceInfo],
        BaseNamesReferenceStyle[ReferenceInfo],
        BaseBracketReferenceStyle[ReferenceInfo],
):

    def __post_init__(self):
        self.styles.extend([
            BasicLabelReferenceStyle(
                ReferenceText=self.ReferenceText,
                name_style_plugin=self.name_style_plugin,
                abbreviate_names=self.abbreviate_names,
                left_bracket=self.left_bracket,
                right_bracket=self.right_bracket,
                outer_separators=self.outer_separators,
                names_separators=self.names_separators,
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
