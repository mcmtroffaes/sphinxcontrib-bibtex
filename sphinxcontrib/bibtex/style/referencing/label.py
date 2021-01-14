import dataclasses

from sphinxcontrib.bibtex.style.referencing import (
    ReferenceInfo, BracketReferenceStyleMixin, NamesReferenceStyleMixin,
    GroupReferenceStyle
)
from .basic_label import BasicLabelReferenceStyle
from .extra_author import ExtraAuthorReferenceStyle
from .extra_label import ExtraLabelReferenceStyle
from .extra_year import ExtraYearReferenceStyle


@dataclasses.dataclass(frozen=True)
class LabelReferenceStyle(
        GroupReferenceStyle[ReferenceInfo],
        NamesReferenceStyleMixin[ReferenceInfo],
        BracketReferenceStyleMixin[ReferenceInfo]):
    """Textual or parenthetical reference by label,
    or just by author, label, or year.
    """

    def __post_init__(self):
        self.styles.extend([
            BasicLabelReferenceStyle(
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
