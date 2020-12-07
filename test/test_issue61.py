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
    output = (app.outdir / "index.html").read_text(encoding='utf-8')
    assert re.search(
        'class="bibtex reference internal" href="#testone"', output)
    assert re.search(
        'class="bibtex reference internal" href="#testtwo"', output)
