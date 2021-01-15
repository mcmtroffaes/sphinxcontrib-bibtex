import dataclasses

from sphinxcontrib.bibtex.style.referencing import (
    BracketStyle, PersonStyle, GroupReferenceStyle
)
from .basic_label import (
    BasicLabelParentheticalReferenceStyle,
    BasicLabelTextualReferenceStyle,
)
from .extra_author import ExtraAuthorReferenceStyle
from .extra_label import ExtraLabelReferenceStyle
from .extra_year import ExtraYearReferenceStyle


@dataclasses.dataclass
class LabelReferenceStyle(GroupReferenceStyle):
    """Textual or parenthetical reference by label,
    or just by author, label, or year.
    """

    #: Bracket style.
    bracket: BracketStyle = BracketStyle()

    #: Person style.
    person: PersonStyle = PersonStyle()

    def __post_init__(self):
        self.styles.extend([
            BasicLabelParentheticalReferenceStyle(
                bracket=self.bracket, person=self.person),
            BasicLabelTextualReferenceStyle(
                bracket=self.bracket, person=self.person),
            ExtraAuthorReferenceStyle(
                bracket=self.bracket, person=self.person),
            ExtraLabelReferenceStyle(bracket=self.bracket),
            ExtraYearReferenceStyle(bracket=self.bracket),
        ])
        super().__post_init__()
