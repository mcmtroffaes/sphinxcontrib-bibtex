extensions = ['sphinxcontrib.bibtex']
source_suffix = '.rst'
exclude_patterns = ['_build']
latex_elements = {
}
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
