# -*- coding: utf-8 -*-
"""
    test_issue187
    ~~~~~~~~~~~~~

    Test multiple footbibliography directives.
"""

import pytest
import re


@pytest.mark.sphinx('html', testroot='issue187')
def test_issue187(app, warning):
    app.builder.build_all()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text(encoding='utf-8')
    assert len(re.findall(
        'id="bibtex-footbibliography-index-0"', output)) == 1
    assert len(re.findall(
        'id="bibtex-footbibliography-index-1"', output)) == 1
    assert len(re.findall(
        'id="bibtex-footbibliography-index-2"', output)) == 1
    assert len(re.findall('id="mandel"', output)) == 1
    assert len(re.findall('id="evensen"', output)) == 1
    assert len(re.findall('id="lorenc"', output)) == 1
    assert len(re.findall(
        'class="footnote-reference brackets" href="#mandel"', output)) == 2
    assert len(re.findall(
        'class="footnote-reference brackets" href="#evensen"', output)) == 1
    assert len(re.findall(
        'class="footnote-reference brackets" href="#lorenc"', output)) == 1
