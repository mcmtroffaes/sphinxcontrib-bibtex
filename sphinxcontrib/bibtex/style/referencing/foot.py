import dataclasses

from . import PersonStyle, GroupReferenceStyle, BracketStyle
from .basic_foot import (
    BasicFootParentheticalReferenceStyle,
    BasicFootTextualReferenceStyle,
)


@dataclasses.dataclass
class FootReferenceStyle(GroupReferenceStyle):
    """Textual or parenthetical reference using footnotes."""

    #: Bracket style for textual citations (:cite:t: and variations).
    bracket_textual: BracketStyle = BracketStyle()

    #: Person style (applies to all relevant citation commands).
    person: PersonStyle = PersonStyle()

    def __post_init__(self):
        self.styles.extend([
            BasicFootParentheticalReferenceStyle(),
            BasicFootTextualReferenceStyle(
                bracket=self.bracket_textual, person=self.person),
        ])
        super().__post_init__()
