"""
    test_custom_labels
    ~~~~~~~~~~~~~~~~~~

    Test a custom label style.
"""

import common
import pytest


@pytest.mark.sphinx('html', testroot='custom_labels')
def test_custom_labels(app, warning):
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text()
    # the custom style uses keys as labels
    # citations
    assert len(common.html_citations(
        label='myfancybibtexkey').findall(output)) == 1
    assert len(common.html_citations(
        label='myotherfancybibtexkey').findall(output)) == 1
    assert len(common.html_citation_refs(
        label='myfancybibtexkey').findall(output)) == 1
    assert len(common.html_citation_refs(
        label='myotherfancybibtexkey').findall(output)) == 1
