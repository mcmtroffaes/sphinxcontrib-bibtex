# -*- coding: utf-8 -*-
"""
    test_filter_syntax_error
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Test response on syntax errors in filter.
"""

import pytest
import re


@pytest.mark.sphinx('html', testroot='filter_syntax_error')
def test_filter_syntax_error(app, warning):
    app.builder.build_all()
    assert len(re.findall(
            'syntax error in :filter: expression', warning.getvalue())) == 9
