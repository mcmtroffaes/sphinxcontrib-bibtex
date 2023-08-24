import re

needs_sphinx = "2.1"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.coverage",
    "sphinx.ext.viewcode",
]
master_doc = "index"
project = "sphinxcontrib-bibtex"
copyright = "2011-2023, Matthias C. M. Troffaes"
with open("../src/sphinxcontrib/bibtex/__init__.py", "rt") as version_file:
    release = re.search('"version": "(.+)"', version_file.read()).group(1)
version = ".".join(release.split(".")[:2])
exclude_patterns = ["_build"]
pygments_style = "sphinx"
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("http://www.sphinx-doc.org/en/master/", None),
}
html_theme = "alabaster"
