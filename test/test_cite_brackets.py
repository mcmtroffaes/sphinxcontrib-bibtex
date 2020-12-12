# -*- coding: utf-8 -*-
"""
    test_cite_brackets
    ~~~~~~~~~~~~~~~~~~

    Test custom cite brackets.
"""

import pytest


@pytest.mark.sphinx('html', testroot='cite_brackets')
def test_cite_brackets(app, warning):
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text(encoding='utf-8')
    assert "&lt;Huy57&gt;" in output
