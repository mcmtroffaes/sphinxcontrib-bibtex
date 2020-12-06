import os, sys
sys.path.append(os.path.dirname(__file__))
extensions = ['sphinxcontrib.bibtex', 'sphinxcontrib.bibtex2', 'sphinx.ext.autodoc']
exclude_patterns = ['_build']
bibtex_bibfiles = ['test.bib']
