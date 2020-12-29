"""
    test_issue15
    ~~~~~~~~~~~~

    Test order of bibliography entries when using an unsorted style.
"""

import pytest
import re


@pytest.mark.sphinx('html', testroot='issue15')
def test_entries_order(app, warning):
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text()
    assert re.search(
        '<dd>.*Test 1.*</dd>.*<dd>.*Test 2.*</dd>',
        output, re.DOTALL)
