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

    #: Bracket style for textual citations (:cite:t: and variations).
    bracket_textual: BracketStyle = BracketStyle()

    #: Bracket style for parenthetical citations
    #: (:cite:p: and variations).
    bracket_parenthetical: BracketStyle = BracketStyle()

    #: Bracket style for author citations
    #: (:cite:author: and variations).
    bracket_author: BracketStyle = BracketStyle()

    #: Bracket style for label citations
    #: (:cite:label: and variations).
    bracket_label: BracketStyle = BracketStyle()

    #: Bracket style for year citations
    #: (:cite:year: and variations).
    bracket_year: BracketStyle = BracketStyle()

    #: Person style.
    person: PersonStyle = PersonStyle()

    def __post_init__(self):
        self.styles.extend([
            BasicLabelParentheticalReferenceStyle(
                bracket=self.bracket_parenthetical, person=self.person),
            BasicLabelTextualReferenceStyle(
                bracket=self.bracket_textual, person=self.person),
            ExtraAuthorReferenceStyle(
                bracket=self.bracket_author, person=self.person),
            ExtraLabelReferenceStyle(bracket=self.bracket_label),
            ExtraYearReferenceStyle(bracket=self.bracket_year),
        ])
        super().__post_init__()
