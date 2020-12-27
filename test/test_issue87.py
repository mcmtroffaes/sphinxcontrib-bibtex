"""
    test_issue87
    ~~~~~~~~~~~~

    Test keyprefix feature.
"""

import common
import pytest


@pytest.mark.sphinx('html', testroot='issue87')
def test_keyprefix(app, warning):
    app.builder.build_all()
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
