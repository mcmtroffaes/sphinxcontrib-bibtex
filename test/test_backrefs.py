"""Test back references."""

import common
import pytest


@pytest.mark.sphinx('html', testroot='backrefs')
def test_backrefs(app, warning):
    app.build()
    output = (app.outdir / "index.html").read_text()
    match = common.html_citations(name="test").search(output)
    assert match
