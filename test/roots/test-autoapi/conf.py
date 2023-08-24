extensions = ["sphinxcontrib.bibtex", "autoapi.extension"]
exclude_patterns = ["_build"]
bibtex_bibfiles = ["test.bib"]
autoapi_dirs = ["some_module/"]
autoapi_keep_files = True  # useful for debugging
autoapi_add_toctree_entry = False