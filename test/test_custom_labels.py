"""
    test_bibliography_style_label_1
    ~~~~~~~~~~~~~~~~~~

    Test a custom label style.
"""

import common
import pytest


@pytest.mark.sphinx('html', testroot='bibliography_style_label_1')
def test_bibliography_style_label_1(app, warning):
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
