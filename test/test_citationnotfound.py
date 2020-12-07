# -*- coding: utf-8 -*-
"""
    test_citationnotfound
    ~~~~~~~~~~~~~~~~~~~~~

    Citation not found check.
"""

import pytest
import re


@pytest.mark.sphinx('html', testroot='citationnotfound')
def test_citationnotfound(app, warning):
    app.builder.build_all()
    assert re.search(
        'citation not found: nosuchkey1', warning.getvalue())
    assert re.search(
        'could not find bibtex key nosuchkey2', warning.getvalue())
