import os
import sys
sys.path.append(os.path.dirname(__file__))
extensions = [
    'sphinxcontrib.bibtex', 'sphinx.ext.autodoc']
exclude_patterns = ['_build']
bibtex_bibfiles = ['test.bib']
autoclass_content = 'both'  # document __init__ method too
