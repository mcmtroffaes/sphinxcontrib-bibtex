# -*- coding: utf-8 -*-
"""
    test_natbib
    ~~~~~~~~~~~

    Test the natbib extension, which serves as an example for comparison.
"""

import pytest
import os
import sys

sys.path.append(os.path.dirname(__file__))  # ensure natbib extension is found


@pytest.mark.sphinx('html', testroot='natbib')
def test_natbib(app, warning):
    app.build()
    assert not warning.getvalue()


@pytest.mark.sphinx('latex', testroot='natbib')
def test_natbib_latex(app, warning):
    app.build()
    assert not warning.getvalue()


@pytest.mark.sphinx('html', testroot='natbib_keynotfound')
def test_natbib_keynotfound(app, warning):
    app.build()
    warning.seek(0)
    warnings = warning.readlines()
    assert len(warnings) == 1
    assert "WARNING: cite-key `XXX` not found in bibtex file" in warnings[0]


@pytest.mark.sphinx('html', testroot='natbib_norefs')
def test_natbib_norefs(app, warning):
    app.build()
    warning.seek(0)
    warnings = warning.readlines()
    assert len(warnings) == 1
    assert "WARNING: no `refs` directive found" in warnings[0]
