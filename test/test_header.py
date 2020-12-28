"""
    test_header
    ~~~~~~~~~~~

    Test header config.
"""

import pytest
import re


@pytest.mark.sphinx('html', testroot='header')
def test_header(app, warning):
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text(encoding='utf-8')
    pattern1 = (
        '<p class="rubric" '
        'id="[^"]+">Regular Citations</p>')
    pattern2 = (
        '<p class="rubric" '
        'id="[^"]+">Footnote Citations</p>')
    assert re.search(pattern1, output) is not None
    assert re.search(pattern2, output) is not None
