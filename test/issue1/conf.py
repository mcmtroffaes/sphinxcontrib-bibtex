import tinkerer
import tinkerer.paths
project = 'My blog'
tagline = 'Add intelligent tagline here'
author = 'Mr Test'
website = 'http://127.0.0.1/blog/html/'
html_theme = "modern5"
posts_per_page = 2

extensions = [
    'sphinxcontrib.bibtex',
    'tinkerer.ext.blog',
    'tinkerer.ext.disqus']

html_static_path = [tinkerer.paths.static]
html_theme_path = [tinkerer.paths.themes]
exclude_patterns = ["drafts/*"]

# **************************************************************
# Do not modify below lines as the values are required by
# Tinkerer to play nice with Sphinx
# **************************************************************

master_doc = tinkerer.master_doc
html_title = project
html_use_index = False
html_show_sourcelink = False
html_add_permalinks = ""
