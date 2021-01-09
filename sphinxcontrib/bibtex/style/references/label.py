from pybtex.style.template import join, sentence, words, names
from . import BaseReferenceStyle, reference, label


class LabelParentheticalReferenceStyle(BaseReferenceStyle):
    """Simple parenthetical references by label."""

    def get_outer_template(self, children, capfirst=False):
        return join[
            self.left_bracket,
            join(sep=',')[children],
            self.right_bracket,
        ]

    def get_inner_template(self):
        return reference[label]


class LabelTextualReferenceStyle(BaseReferenceStyle):
    """Simple textual references by last name and label."""

    def get_outer_template(self, children, capfirst=False):
        return sentence(
            capfirst=capfirst, add_period=False, sep='; ')[children]

    def get_inner_template(self):
        return words[
             names('author', sep=', ', sep2=' and ', last_sep=', and'),
             join[
                 self.left_bracket,
                 reference[label],
                 self.right_bracket
             ]
        ]
