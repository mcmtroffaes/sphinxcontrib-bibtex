# -*- coding: utf-8 -*-
"""
    test_latex_refs
    ~~~~~~~~~~~~~~~

    Check that LaTeX backend produces correct references.
"""

import pytest


@pytest.mark.sphinx('latex', testroot='latex_refs')
def test_latex_refs(app, warning):
    app.builder.build_all()
    assert not warning.getvalue()
    output = (app.outdir / "test.tex").read_text(encoding='utf-8')
    assert r'\sphinxcite{index:huygens}' in output
    assert r'\bibitem[Huy57]{index:huygens}' in output
