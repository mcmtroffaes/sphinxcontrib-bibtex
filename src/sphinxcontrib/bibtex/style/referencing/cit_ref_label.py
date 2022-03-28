from dataclasses import dataclass, field
from typing import Union, TYPE_CHECKING

from sphinxcontrib.bibtex.style.referencing import (
    BracketStyle, PersonStyle, GroupReferenceStyle
)
from .basic_cit_ref_label import (
    BasicCitRefLabelParentheticalReferenceStyle,
    BasicCitRefLabelTextualReferenceStyle,
)
from .extra_empty import ExtraEmptyReferenceStyle

if TYPE_CHECKING:
    from pybtex.richtext import BaseText


@dataclass
class CitRefLabelReferenceStyle(GroupReferenceStyle):
    """Textual or parenthetical reference by label,
    or just by author, label, or year.
    """

    #: Bracket style for textual citations (:cite:t: and variations).
    #: Note: brackets are ignored, only separators are used.
    bracket_textual: BracketStyle = field(default_factory=BracketStyle)

    #: Person style.
    person: PersonStyle = field(default_factory=PersonStyle)

    #: Separator between labels for parenthetical citations.
    label_sep_parenthetical: Union["BaseText", str] = ' '

    #: Separator between text and reference for textual citations.
    text_reference_sep: Union["BaseText", str] = ' '

    def __post_init__(self):
        self.styles.extend([
            BasicCitRefLabelParentheticalReferenceStyle(),
            BasicCitRefLabelTextualReferenceStyle(
                bracket=self.bracket_textual,
                person=self.person,
                text_reference_sep=self.text_reference_sep,
            ),
            ExtraEmptyReferenceStyle(),
        ])
        super().__post_init__()
