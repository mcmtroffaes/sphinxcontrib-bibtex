extensions = ['sphinxcontrib.bibtex']
source_suffix = '.rst'
master_doc = 'index'
exclude_patterns = ['_build']
latex_elements = {
}
latex_documents = [
    ('index', 'test.tex', u'test Documentation',
     u'nobody', 'manual'),
]
man_pages = [
    ('index', 'test', u'test Documentation',
     [u'nobody'], 1)
]
texinfo_documents = [
    ('index', 'test', u'test Documentation',
     u'nobody', 'test', 'One line description of project.',
     'Miscellaneous'),
]
