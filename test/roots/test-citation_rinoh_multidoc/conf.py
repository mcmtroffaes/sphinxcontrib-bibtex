extensions = ["rinoh.frontend.sphinx", "sphinxcontrib.bibtex"]
exclude_patterns = ["_build"]
bibtex_bibfiles = ["test.bib"]
rinoh_documents = [
    dict(doc="index", target="book", toctree_only=False, template="template.rtt"),
]
