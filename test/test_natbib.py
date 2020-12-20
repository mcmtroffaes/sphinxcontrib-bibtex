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
    warning.seek(0)
    warnings = warning.readlines()
    assert len(warnings) == 1
    assert "natbib/doc0.rst:18: WARNING: cite-key `XXX` not found in bibtex file" in warnings[0]
