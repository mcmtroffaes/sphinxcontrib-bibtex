extensions = ['sphinxcontrib.bibtex']
source_suffix = '.rst'
master_doc = 'index'
copyright = u'2012, nobody'
exclude_patterns = ['_build']
pygments_style = 'sphinx'
html_theme = 'default'
htmlhelp_basename = 'testdoc'
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

# create and register pybtex plugins

import pkg_resources
for dist in pkg_resources.find_distributions("plugins/"):
    pkg_resources.working_set.add(dist)
