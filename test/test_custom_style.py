"""
    test_custom_style
    ~~~~~~~~~~~~~~~~~

    Test a custom style.
"""

import pytest


@pytest.mark.sphinx('html', testroot='custom_style')
def test_custom_style(app, warning):
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text(encoding='utf-8')
    # the custom style suppresses web links
    assert 'http://arxiv.org' not in output
    assert 'http://dx.doi.org' not in output
