# -*- coding: utf-8 -*-
"""
    test_issue17
    ~~~~~~~~~~~~

    Test that sphinx [source] links do not generate a warning.
"""

import pytest


@pytest.mark.sphinx('html', testroot='issue17')
def test_sphinx_source_no_warning(app, warning):
    app.builder.build_all()
    assert not warning.getvalue()
