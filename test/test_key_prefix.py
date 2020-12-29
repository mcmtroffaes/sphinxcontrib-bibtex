import common
import pytest


# see issue 87
@pytest.mark.sphinx('html', testroot='key_prefix')
def test_key_prefix(app, warning):
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "doc0.html").read_text()
    cits = {match.group('label')
            for match in common.html_citations().finditer(output)}
    citrefs = {match.group('label')
               for match in common.html_citation_refs().finditer(output)}
    assert cits == citrefs == {'AMan09', 'AEve03'}
    output = (app.outdir / "doc1.html").read_text()
    cits = {match.group('label')
            for match in common.html_citations().finditer(output)}
    citrefs = {match.group('label')
               for match in common.html_citation_refs().finditer(output)}
    assert cits == citrefs == {'BMan09'}
