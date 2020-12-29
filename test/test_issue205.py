"""
    test_issue205
    ~~~~~~~~~~~~~

    Test cites spanning multiple lines.
"""

import common
import pytest


@pytest.mark.sphinx('html', testroot='issue205')
def test_issue205(app, warning):
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text()
    # ensure Man09 is cited
    assert len(common.html_citation_refs(label='Fir').findall(output)) == 1
    assert len(common.html_citation_refs(label='Sec').findall(output)) == 1
