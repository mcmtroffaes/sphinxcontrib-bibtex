from pybtex.style.formatting.unsrt import Style as UnsrtStyle
from pybtex.style.template import words
from pybtex.plugin import register_plugin


extensions = ['sphinxcontrib.bibtex']
exclude_patterns = ['_build']


class NoWebRefStyle(UnsrtStyle):

    def format_web_refs(self, e):
        # the following is just one simple way to return an empty node
        return words['']


register_plugin('pybtex.style.formatting', 'nowebref', NoWebRefStyle)
