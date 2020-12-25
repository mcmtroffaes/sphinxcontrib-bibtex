"""
    test_latex_refs
    ~~~~~~~~~~~~~~~

    Check that LaTeX backend produces correct references.
"""

import pytest


@pytest.mark.sphinx('latex', testroot='latex_refs')
def test_latex_refs(app, warning):
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "test.tex").read_text()
    assert r'\sphinxcite{index:bibtex-citation-huygens}' in output
    assert r'\bibitem[Huy57]{index:bibtex-citation-huygens}' in output
