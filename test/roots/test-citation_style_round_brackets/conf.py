import dataclasses
import sphinxcontrib.bibtex.plugin

from sphinxcontrib.bibtex.style.referencing.author_year \
    import AuthorYearReferenceStyle


@dataclasses.dataclass
class MyReferenceStyle(AuthorYearReferenceStyle):
    left_bracket: str = '('
    right_bracket: str = ')'


sphinxcontrib.bibtex.plugin.register_plugin(
    'sphinxcontrib.bibtex.style.referencing',
    'author_year_round', MyReferenceStyle)

extensions = ['sphinxcontrib.bibtex']
exclude_patterns = ['_build']
bibtex_bibfiles = ['refs.bib']
bibtex_reference_style = 'author_year_round'
