# -*- coding: utf-8 -*-
"""
    test_issue_173
    ~~~~~~~~~~~~~~

    Check referencing works with near identical entries.
"""

import pytest


@pytest.mark.sphinx('html', testroot='issue_173')
def test_issue_173(app, warning):
    app.builder.build_all()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text(encoding='utf-8')
    assert "[xyz19a]" in output
    assert "[xyz19b]" in output
