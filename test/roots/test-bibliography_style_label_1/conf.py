from pybtex.plugin import register_plugin
from pybtex.style.formatting.unsrt import Style as UnsrtStyle
from pybtex.style.labels import BaseLabelStyle

extensions = ["sphinxcontrib.bibtex"]
exclude_patterns = ["_build"]
bibtex_bibfiles = ["test.bib"]
bibtex_default_style = "mystyle"


# a simple label style which uses the bibtex keys for labels
class MyLabelStyle(BaseLabelStyle):
    def format_labels(self, sorted_entries):
        for entry in sorted_entries:
            yield entry.key


class MyStyle(UnsrtStyle):
    default_label_style = MyLabelStyle


register_plugin("pybtex.style.formatting", "mystyle", MyStyle)
