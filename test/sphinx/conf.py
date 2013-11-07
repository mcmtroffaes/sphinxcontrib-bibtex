extensions = ['sphinxcontrib.bibtex']
source_suffix = '.rst'
master_doc = 'index'
copyright = u'2011, Matthias C. M. Troffaes'
exclude_patterns = ['_build']
pygments_style = 'sphinx'
html_theme = 'default'
htmlhelp_basename = 'Sphinxbibtexextensiontestdoc'
latex_documents = [
    ('index', 'Sphinxbibtexextensiontest.tex',
     u'Sphinx bibtex extension test Documentation',
     u'Matthias C. M. Troffaes', 'manual'),
]
man_pages = [
    ('index', 'sphinxbibtexextensiontest',
     u'Sphinx bibtex extension test Documentation',
     [u'Matthias C. M. Troffaes'], 1)
]
