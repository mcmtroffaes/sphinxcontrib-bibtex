import sys
import os
# viewcode extension specifically needed for this test
extensions = [
    'sphinxcontrib.bibtex',
    'sphinx.ext.viewcode',
    'sphinx.ext.autodoc']
bibtex_bibfiles = []
# make sure we find the module
sys.path.insert(0, os.path.abspath('.'))

exclude_patterns = ['_build']
