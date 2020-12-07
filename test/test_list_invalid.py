# -*- coding: utf-8 -*-
"""
    test_list_invalid
    ~~~~~~~~~~~~~~~~~

    Test invalid ``:list:`` option.
"""

import pytest
import re


@pytest.mark.sphinx('html', testroot='list_invalid')
def test_list_invalid(app, warning):
    app.builder.build_all()
    assert re.search(
        "unknown bibliography list type 'thisisintentionallyinvalid'",
        warning.getvalue())
