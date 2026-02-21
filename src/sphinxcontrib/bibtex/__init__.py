"""
.. autofunction:: setup
"""

import sys
from typing import Any, Dict, Sequence

if sys.version_info >= (3, 10):
    from importlib.metadata import version
else:
    from importlib_metadata import version

from sphinx.application import Sphinx

from .directives import BibliographyDirective
from .domain import BibtexDomain
from .foot_directives import FootBibliographyDirective
from .foot_domain import BibtexFootDomain
from .foot_roles import FootCiteRole
from .nodes import bibliography, depart_raw_latex, raw_latex, visit_raw_latex
from .roles import CiteRole
from .transforms import BibliographyTransform

_footcite_roles: Sequence[str] = ["p", "ps", "t", "ts", "ct", "cts"]
_cite_roles: Sequence[str] = list(_footcite_roles) + [
    "empty",
    "alp",
    "alps",
    "label",
    "labelpar",
    "year",
    "yearpar",
    "author",
    "authors",
    "authorpar",
    "authorpars",
    "cauthor",
    "cauthors",
]


def setup(app: Sphinx) -> Dict[str, Any]:
    """Set up the bibtex extension:

    * register config values
    * register directives
    * register nodes
    * register roles
    * register transforms
    * connect events to functions
    """
    app.add_config_value("bibtex_default_style", "alpha", "html")
    app.add_config_value("bibtex_tooltips", True, "html")
    app.add_config_value("bibtex_tooltips_style", "", "html")
    app.add_config_value("bibtex_bibfiles", None, "html")
    app.add_config_value("bibtex_encoding", "utf-8-sig", "html")
    app.add_config_value("bibtex_bibliography_header", "", "html")
    app.add_config_value("bibtex_footbibliography_header", "", "html")
    app.add_config_value("bibtex_reference_style", "label", "env")
    app.add_config_value("bibtex_foot_reference_style", "foot", "env")
    app.add_config_value("bibtex_cite_id", "", "html")
    app.add_config_value("bibtex_footcite_id", "", "html")
    app.add_config_value("bibtex_bibliography_id", "", "html")
    app.add_config_value("bibtex_footbibliography_id", "", "html")
    app.add_domain(BibtexDomain)
    app.add_directive("bibliography", BibliographyDirective)
    app.add_role("cite", CiteRole())
    for role_name in _cite_roles:
        app.add_role_to_domain("cite", role_name, CiteRole())
    app.add_node(bibliography, override=True)
    app.add_node(raw_latex, latex=(visit_raw_latex, depart_raw_latex), override=True)
    app.add_post_transform(BibliographyTransform)
    app.add_domain(BibtexFootDomain)
    app.add_directive("footbibliography", FootBibliographyDirective)
    app.add_role("footcite", FootCiteRole())
    for role_name in _footcite_roles:
        app.add_role_to_domain("footcite", role_name, FootCiteRole())
    return {
        "version": version("sphinxcontrib-bibtex"),
        "env_version": 9,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
