"""
Unsorted pybtex style.

Adapted from pybtex/style/formatting/unsrt.py.
"""

from pybtex.style.formatting.unsrt import Style as BaseStyle
from pybtex.style.formatting import toplevel
from pybtex.style.template import (
    join, words, field, optional, first_of,
    names, sentence, tag, optional_field
)

class Style(BaseStyle):
    name = 'unsrt_'

    # TODO complete the following
    
    def format_incollection(self, e):
        template = toplevel [
            sentence [self.format_names('author')],
            sentence [field('title')],
        ]
        return template.format_data(e)

    def format_inproceedings(self, e):
        template = toplevel [
            sentence [self.format_names('author')],
            sentence [field('title')],
        ]
        return template.format_data(e)

    def format_manual(self, e):
        template = toplevel [
            sentence [self.format_names('author')],
            sentence [field('title')],
        ]
        return template.format_data(e)

    def format_mastersthesis(self, e):
        template = toplevel [
            sentence [self.format_names('author')],
            sentence [field('title')],
        ]
        return template.format_data(e)

    def format_phdthesis(self, e):
        template = toplevel [
            sentence [self.format_names('author')],
            sentence [field('title')],
        ]
        return template.format_data(e)

    def format_proceedings(self, e):
        template = toplevel [
            sentence [self.format_names('editor')],
            sentence [field('title')],
        ]
        return template.format_data(e)

    def format_techreport(self, e):
        template = toplevel [
            sentence [self.format_names('author')],
            sentence [field('title')],
        ]
        return template.format_data(e)

    def format_unpublished(self, e):
        template = toplevel [
            sentence [self.format_names('author')],
            sentence [field('title')],
        ]
        return template.format_data(e)

    def format_misc(self, e):
        template = toplevel [
            sentence [self.format_names('author')],
            sentence [field('title')],
        ]
        return template.format_data(e)
