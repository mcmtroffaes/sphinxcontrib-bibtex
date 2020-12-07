# -*- coding: utf-8 -*-
"""
    test_json
    ~~~~~~~~~~~

    Test json and check output.
"""

import pytest


@pytest.mark.sphinx('html', testroot='json')
def test_json(app, warning):
    app.build()
    warnings = warning.getvalue()
    assert "citation not found: first" in warnings
    assert "rerun sphinx build" in warnings
