import sys, os
extensions = ['sphinxcontrib.bibtex']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'Sphinx bibtex extension test'
copyright = u'2011, Matthias C. M. Troffaes'
version = '1.0'
release = '1.0'
exclude_patterns = ['_build']
pygments_style = 'sphinx'
html_theme = 'default'
htmlhelp_basename = 'Sphinxbibtexextensiontestdoc'
latex_documents = [
  ('index', 'Sphinxbibtexextensiontest.tex', u'Sphinx bibtex extension test Documentation',
   u'Matthias C. M. Troffaes', 'manual'),
]
man_pages = [
    ('index', 'sphinxbibtexextensiontest', u'Sphinx bibtex extension test Documentation',
     [u'Matthias C. M. Troffaes'], 1)
]
