# -*- coding: utf-8 -*-
"""
    test_json
    ~~~~~~~~~~~

    Test json and check output.
"""

import json
import pytest
import shutil


@pytest.mark.sphinx('html', testroot='json')
def test_json(make_app, app_params):
    args, kwargs = app_params
    app1 = make_app(*args, **kwargs)
    try:
        (app1.srcdir / "bibtex.json").unlink()
    except FileNotFoundError:
        pass
    app1.build()
    output = (app1.outdir / "index.html").read_text()
    warnings = app1._warning.getvalue()
    assert "citation not found: first" in warnings
    assert "run 'sphinx-build -E ...' for a fresh rebuild" in warnings
    assert "[first]" in output
    assert "[1]" not in output
    assert "A. First. Test 1." not in output
    assert json.loads((app1.srcdir / "bibtex.json").read_text()) == {'cited': {'index': ['first']}}
    app2 = make_app(*args, freshenv=True, **kwargs)
    app2.build()
    output2 = (app2.outdir / "index.html").read_text()
    warnings2 = app2._warning.getvalue()
    assert "citation not found: first" not in warnings2
    assert "run 'sphinx-build -E ...' for a fresh rebuild" not in warnings2
    assert "[first]" not in output2
    assert "[1]" in output2
    assert "A. First. Test 1." in output2
    (app2.srcdir / "bibtex.json").unlink()
