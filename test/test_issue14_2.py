"""
    test_issue14_2
    ~~~~~~~~~~~~~~

    Test labelprefix option.
"""

import common
import pytest


@pytest.mark.sphinx('html', testroot='issue14_2')
def test_label_prefix(app, warning):
    app.builder.build_all()
    assert not warning.getvalue()
    output = (app.outdir / "doc1.html").read_text()
    assert common.html_citation_refs(label="A1").search(output)
    output = (app.outdir / "doc2.html").read_text()
    assert common.html_citation_refs(label="B1").search(output)
