extensions = ['sphinxcontrib.bibtex']
source_suffix = '.rst'
exclude_patterns = ['_build']
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
