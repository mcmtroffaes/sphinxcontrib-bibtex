# -*- coding: utf-8 -*-
"""
    test_custom_style
    ~~~~~~~~~~~~~~~~~

    Test a custom style.
"""

import re
import pytest


@pytest.mark.sphinx('html', testroot='custom_style')
def test_custom_style(app, warning):
    app.builder.build_all()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text(encoding='utf-8')
    # the custom style suppresses web links
    assert not re.search('http://arxiv.org', output)
    assert not re.search('http://dx.doi.org', output)
