extensions = ['sphinxcontrib.bibtex']
exclude_patterns = ['_build']

# create and register pybtex plugins

from pybtex.style.formatting.unsrt import Style as UnsrtStyle
from pybtex.style.template import words
from pybtex.plugin import plugin_registry_loader

class NoWebRefStyle(UnsrtStyle):
    name = 'nowebref'

    def format_web_refs(self, e):
        # the following is just one simple way to return an empty node
        return words['']

plugin_registry_loader.register_name(
    'pybtex.style.formatting', 'nowebref', NoWebRefStyle)
