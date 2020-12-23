# -*- coding: utf-8 -*-
"""
    test_sphinx
    ~~~~~~~~~~~

    General Sphinx test and check output.
"""
from typing import cast

import pytest

from sphinxcontrib.bibtex import BibtexDomain


@pytest.mark.sphinx('html', testroot='sphinx')
def test_sphinx(app, warning):
    app.build()
