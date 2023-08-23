import re

import pytest


@pytest.mark.rinohtype
@pytest.mark.sphinx("rinoh", testroot="citation_rinoh")
def test_citation_rinoh(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "book.stylelog").read_text()
    assert len(re.findall(r"NoteMarkerByID\('tes', style='citation'\)", output)) == 1
    assert len(re.findall(r"DirectReference\('tes'\)", output)) == 1


@pytest.mark.rinohtype
@pytest.mark.sphinx("rinoh", testroot="citation_rinoh_multidoc")
def test_citation_rinoh_multidoc(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "book.stylelog").read_text()
    assert len(re.findall(r"NoteMarkerByID\('tes', style='citation'\)", output)) == 2
    assert len(re.findall(r"DirectReference\('tes'\)", output)) == 1
