# -*- coding: utf-8 -*-
"""
    test_subfolder
    ~~~~~~~~~~~

    Test bib files in subfolder.
"""

import pytest


@pytest.mark.sphinx('html', testroot='subfolder')
def test_sphinx(app, warning):
    app.builder.build_all()
    assert not warning.getvalue()
