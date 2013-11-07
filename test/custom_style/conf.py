extensions = ['sphinxcontrib.bibtex']
exclude_patterns = ['_build']

# create and register pybtex plugins

import pkg_resources
for dist in pkg_resources.find_distributions("plugins/"):
    pkg_resources.working_set.add(dist)
