"""
    test_bibliography_style_nowebref
    ~~~~~~~~~~~~~~~~~

    Test a custom style.
"""

import pytest


@pytest.mark.sphinx('html', testroot='bibliography_style_nowebref')
def test_bibliography_style_nowebref(app, warning):
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text(encoding='utf-8')
    # the custom style suppresses web links
    assert 'http://arxiv.org' not in output
    assert 'http://dx.doi.org' not in output
