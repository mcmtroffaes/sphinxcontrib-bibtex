import dataclasses
import sphinxcontrib.bibtex.plugin

from sphinxcontrib.bibtex.style.referencing import BracketStyle
from sphinxcontrib.bibtex.style.referencing.author_year \
    import AuthorYearReferenceStyle

my_bracket_style = BracketStyle(
    left='(',
    right=')',
)


@dataclasses.dataclass
class MyReferenceStyle(AuthorYearReferenceStyle):
    bracket_parenthetical: BracketStyle = my_bracket_style
    bracket_textual: BracketStyle = my_bracket_style
    bracket_author: BracketStyle = my_bracket_style
    bracket_label: BracketStyle = my_bracket_style
    bracket_year: BracketStyle = my_bracket_style


sphinxcontrib.bibtex.plugin.register_plugin(
    'sphinxcontrib.bibtex.style.referencing',
    'author_year_round', MyReferenceStyle)


extensions = ['sphinxcontrib.bibtex']
exclude_patterns = ['_build']
bibtex_bibfiles = ['refs.bib']
bibtex_reference_style = 'author_year_round'
