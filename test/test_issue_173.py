"""
    test_issue_173
    ~~~~~~~~~~~~~~

    Check referencing works with near identical entries.
"""

import common
import pytest


@pytest.mark.sphinx('html', testroot='issue_173')
def test_issue_173(app, warning):
    app.builder.build_all()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text(encoding='utf-8')
    assert common.html_citation_refs(label="xyz19a").search(output)
    assert common.html_citation_refs(label="xyz19b").search(output)
