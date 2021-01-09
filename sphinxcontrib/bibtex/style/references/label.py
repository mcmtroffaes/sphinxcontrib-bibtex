from pybtex.style.template import join, sentence, words, names
from . import BaseReferenceStyle, reference, entry_label


class LabelParentheticalReferenceStyle(BaseReferenceStyle):
    """Simple parenthetical references by label."""

    references_sep = ','

    def get_outer_template(self, children, capfirst=False):
        return join[
            self.left_bracket,
            join(sep=self.references_sep)[children],
            self.right_bracket,
        ]

    def get_inner_template(self):
        return reference[entry_label]


class LabelTextualReferenceStyle(BaseReferenceStyle):
    """Simple textual references by last name and label."""

    references_sep = '; '
    names_sep = ', '
    names_sep2 = ' and '
    names_last_sep = ', and '

    def get_outer_template(self, children, capfirst=False):
        return sentence(
            capfirst=capfirst,
            add_period=False,
            sep=self.references_sep)[children]

    def get_inner_template(self):
        return words[
             names('author', sep=self.names_sep, sep2=self.names_sep2,
                   last_sep=self.names_last_sep),
             join[
                 self.left_bracket,
                 reference[entry_label],
                 self.right_bracket
             ]
        ]
