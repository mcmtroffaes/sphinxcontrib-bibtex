# -*- coding: utf-8 -*-
"""
    test_custom_labels
    ~~~~~~~~~~~~~~~~~~

    Test a custom label style.
"""

import pytest


@pytest.mark.sphinx('html', testroot='custom_labels')
def test_custom_labels(app, warning):
    app.builder.build_all()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text(encoding='utf-8')
    # the custom style uses keys as labels
    assert "[myfancybibtexkey]" in output
    assert "[myotherfancybibtexkey]" in output
    assert ">myfancybibtexkey</a>" in output
    assert ">myotherfancybibtexkey</a>" in output
