# -*- coding: utf-8 -*-
"""
    test_footnote
    ~~~~~~~~~~~~~

    Test for footbib.
"""

import pytest


@pytest.mark.sphinx('html', testroot='footnote')
def test_footnote(app, warning):
    app.parallel = 4
    app.builder.build_all()
    assert not warning.getvalue()
