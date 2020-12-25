"""
    test_custom_labels
    ~~~~~~~~~~~~~~~~~~

    Test a custom label style.
"""

import pytest


@pytest.mark.sphinx('html', testroot='custom_labels')
def test_custom_labels(app, warning):
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text()
    # the custom style uses keys as labels
    # citations
    assert ">myfancybibtexkey</span>" in output
    assert ">myotherfancybibtexkey</span>" in output
    # citation_refs
    assert ">[myfancybibtexkey]</a>" in output
    assert ">[myotherfancybibtexkey]</a>" in output
