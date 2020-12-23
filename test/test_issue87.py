"""
    test_issue87
    ~~~~~~~~~~~~

    Test bibliography tags.
"""

import pytest
import re


@pytest.mark.sphinx('html', testroot='issue87')
def test_issue87(app, warning):
    app.builder.build_all()
    assert not warning.getvalue()
    output = (app.outdir / "doc0.html").read_text()
    assert (
        'class="citation-reference" href="#bibtex-citation-tag0-2009-mandel"'
        in output)
    assert (
        'class="citation-reference" href="#bibtex-citation-tag0-2003-evensen"'
        in output)
    assert 'AMan09' in output
    assert 'AEve03' in output
    output = (app.outdir / "doc1.html").read_text()
    assert (
        'class="citation-reference" href="#bibtex-citation-tag1-2009-mandel"'
        in output)
    assert (
        'class="citation-reference" href="#bibtex-citation-tag1-2003-evensen"'
        not in output)
    assert 'BMan09' in output
    assert 'BEve03' not in output
