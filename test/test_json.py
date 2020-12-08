# -*- coding: utf-8 -*-
"""
    test_json
    ~~~~~~~~~~~

    Test json and check output.
"""

import json
import pytest


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
    docoutput = (app1.outdir / "doc.html").read_text()
    warnings = app1._warning.getvalue()
    assert "citation not found: first" in warnings
    assert "citation not found: second" in warnings
    assert "bibtex citations changed, rerun sphinx" in warnings
    assert "[first]" in output
    assert "[1]" not in output
    assert "A. First. Test 1." not in output
    assert "[second]" in output
    assert "[A1]" not in output
    assert "B. Second. Test 2." not in docoutput
    assert \
        json.loads((app1.srcdir / "bibtex.json").read_text()) \
        == {'cited': {'index': ['first', 'second']}}
    app2 = make_app(*args, **kwargs)
    app2.build()
    output2 = (app2.outdir / "index.html").read_text()
    docoutput2 = (app2.outdir / "doc.html").read_text()
    warnings2 = app2._warning.getvalue()
    assert "citation not found: first" not in warnings2
    assert "citation not found: second" not in warnings2
    assert "bibtex citations changed, rerun sphinx" not in warnings2
    assert "[first]" not in output2
    assert "[1]" in output2
    assert "A. First. Test 1." in output2
    assert "[second]" not in output2
    assert "[A1]" in output2
    assert "B. Second. Test 2." in docoutput2
    (app2.srcdir / "bibtex.json").unlink()
