import pybtex.plugin
from pybtex.style.formatting.unsrt import Style as UnsrtStyle
from pybtex.style.template import words

extensions = ["sphinxcontrib.bibtex"]
exclude_patterns = ["_build"]
bibtex_bibfiles = ["test.bib"]
bibtex_default_style = "nowebref"


class NoWebRefStyle(UnsrtStyle):
    def format_web_refs(self, e):
        # the following is just one simple way to return an empty node
        return words[""]


pybtex.plugin.register_plugin("pybtex.style.formatting", "nowebref", NoWebRefStyle)
