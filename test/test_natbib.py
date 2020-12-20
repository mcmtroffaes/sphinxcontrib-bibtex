# -*- coding: utf-8 -*-
"""
    test_natbib
    ~~~~~~~~~~~

    Test the natbib extension, which serves as an example for comparison.
"""

import pytest
import re


@pytest.mark.sphinx('html', testroot='natbib')
def test_natbib(app, warning):
    app.build()
    assert not warning.getvalue()
