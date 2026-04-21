"""
.. autofunction:: setup
"""

from collections.abc import Iterable
from importlib.metadata import version
from pathlib import Path
from typing import Any, Dict, cast

from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment
from sphinx.errors import ExtensionError

from .bibfile import process_bibdata
from .directives import BibliographyDirective
from .domain import BibtexDomain
from .foot_directives import FootBibliographyDirective
from .foot_domain import BibtexFootDomain
from .foot_roles import FootCiteRole
from .nodes import bibliography, depart_raw_latex, raw_latex, visit_raw_latex
from .plugin import find_plugin
from .roles import CiteRole
from .transforms import BibliographyTransform


def env_updated(app: Sphinx, env: BuildEnvironment) -> Iterable[str]:
    dom = cast(BibtexDomain, env.get_domain("cite"))
    return dom.env_updated()


def builder_inited_cite(app: Sphinx) -> None:
    dom = cast(BibtexDomain, app.env.get_domain("cite"))
    # set up referencing style
    style = find_plugin(
        "sphinxcontrib.bibtex.style.referencing",
        app.config.bibtex_reference_style,
    )
    dom.reference_style = style()
    # check config
    if app.config.bibtex_bibfiles is None:
        raise ExtensionError("You must configure the bibtex_bibfiles setting")
    # canonicalize bibfile paths relative to confdir
    bibfiles = [
        (Path(app.confdir) / file).resolve() for file in app.config.bibtex_bibfiles
    ]
    # update bib file information in the cache
    dom.data["bibdata"] = process_bibdata(
        dom.bibdata, bibfiles, app.config.bibtex_encoding
    )


def builder_inited_footcite(app: Sphinx) -> None:
    dom = cast(BibtexDomain, app.env.get_domain("footcite"))
    # set up referencing style
    style = find_plugin(
        "sphinxcontrib.bibtex.style.referencing",
        app.config.bibtex_foot_reference_style,
    )
    dom.reference_style = style()


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
    app.add_node(bibliography, override=True)
    app.add_node(raw_latex, latex=(visit_raw_latex, depart_raw_latex), override=True)
    app.add_post_transform(BibliographyTransform)
    app.add_domain(BibtexFootDomain)
    app.add_directive("footbibliography", FootBibliographyDirective)
    app.add_role("footcite", FootCiteRole())
    app.connect("builder-inited", builder_inited_cite)
    app.connect("builder-inited", builder_inited_footcite)
    app.connect("env-updated", env_updated)
    return {
        "version": version("sphinxcontrib-bibtex"),
        "env_version": 9,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
