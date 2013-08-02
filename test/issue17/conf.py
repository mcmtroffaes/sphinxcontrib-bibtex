import sys
import os
# viewcode extension specifically needed for this test
extensions = [
    'sphinxcontrib.bibtex',
    'sphinx.ext.viewcode',
    'sphinx.ext.autodoc']
# make sure we find the module
sys.path.insert(0, os.path.abspath('.'))

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'test'
copyright = u'2012, nobody'
version = '0'
release = '0'
exclude_patterns = ['_build']
pygments_style = 'sphinx'
html_theme = 'default'
html_static_path = ['_static']
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
