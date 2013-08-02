"""Custom pybtex plugins."""

from pybtex.style.formatting.unsrt import Style as UnsrtStyle
from pybtex.style.template import words


class NoWebRefStyle(UnsrtStyle):
    name = 'nowebref'
    default_name_style = 'lastfirst'  # 'lastfirst' or 'plain'
    default_label_style = 'number'  # 'number' or 'alpha'
    # 'none' or 'author_year_title'
    default_sorting_style = 'author_year_title'

    def format_web_refs(self, e):
        # the following is just one simple way to return an empty node
        return words['']
