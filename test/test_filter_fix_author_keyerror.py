# -*- coding: utf-8 -*-
"""
    test_filter_fix_author_keyerror
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Test for a bug in the filter option.
"""

import pytest


@pytest.mark.sphinx('html', testroot='filter_fix_author_keyerror')
def test_filter_fix_author_keyerror(app):
    app.builder.build_all()
