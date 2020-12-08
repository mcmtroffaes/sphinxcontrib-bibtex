# -*- coding: utf-8 -*-
"""
    test_issue4
    ~~~~~~~~~~~

    Test the ``:encoding:`` option.
"""

import pytest
import re


@pytest.mark.sphinx('html', testroot='issue4')
def test_encoding(app, warning):
    app.builder.build_all()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text(encoding='utf-8')
    assert re.search(u"Tést☺", output)
