import common
import pytest


@pytest.mark.sphinx('html', testroot='citation_multiple_keys')
def test_citation_multiple_keys(app, warning):
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text()
    cits = {match.group('label')
            for match in common.html_citations().finditer(output)}
    citrefs = {match.group('label')
               for match in common.html_citation_refs().finditer(output)}
    assert {"App", "Bra"} == cits == citrefs
