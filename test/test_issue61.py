# -*- coding: utf-8 -*-
"""
    test_issue61
    ~~~~~~~~~~~~

    Test multiple keys in a single cite.
"""

import pytest
import re


@pytest.mark.sphinx('html', testroot='issue61')
def test_multiple_keys(app, warning):
    app.builder.build_all()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text()
    assert re.search(
        'class="citation-reference" href="#.*testone.*"', output)
    assert re.search(
        'class="citation-reference" href="#.*testtwo.*"', output)
