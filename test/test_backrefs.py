"""Test back references."""

from test.common import html_citations
import pytest


@pytest.mark.sphinx('html', testroot='backrefs')
def test_backrefs(app, warning) -> None:
    app.build()
    output = (app.outdir / "index.html").read_text()
    match = html_citations(text=".*Test zero.*").search(output)
    assert match
    assert match.group('backref') is None
    assert match.group('backref1') is None
    assert match.group('backref2') is None
    assert match.group('backref3') is None
    match = html_citations(text=".*Test one.*").search(output)
    assert match
    assert match.group('backref') is not None
    assert match.group('backref1') is None
    assert match.group('backref2') is None
    assert match.group('backref3') is None
    match = html_citations(text=".*Test two.*").search(output)
    assert match
    assert match.group('backref') is None
    assert match.group('backref1') is not None
    assert match.group('backref2') is not None
    assert match.group('backref3') is None
    match = html_citations(text=".*Test three.*").search(output)
    assert match
    assert match.group('backref') is None
    assert match.group('backref1') is not None
    assert match.group('backref2') is not None
    assert match.group('backref3') is not None
