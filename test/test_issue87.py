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
    output = (app.outdir / "doc0.html").read_text(encoding='utf-8')
    assert re.search(
        'class="bibtex reference internal" href="#tag0-2009-mandel"', output)
    assert re.search(
        'class="bibtex reference internal" href="#tag0-2003-evensen"', output)
    assert re.search('AMan09', output)
    assert re.search('AEve03', output)
    output = (app.outdir / "doc1.html").read_text(encoding='utf-8')
    assert re.search(
        'class="bibtex reference internal" href="#tag1-2009-mandel"', output)
    assert not re.search(
        'class="bibtex reference internal" href="#tag1-2003-evensen"', output)
    assert re.search('BMan09', output)
    assert not re.search('BEve03', output)
