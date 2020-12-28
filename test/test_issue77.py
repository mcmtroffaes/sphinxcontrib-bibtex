"""
    test_issue77
    ~~~~~~~~~~~~

    Test label style.
"""

import common
import pytest


@pytest.mark.sphinx('html', testroot='issue77')
def test_issue77(app, warning):
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text()
    assert len(common.html_citation_refs(label='APAa').findall(output)) == 1
    assert len(common.html_citation_refs(label='APAb').findall(output)) == 1
