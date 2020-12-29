"""
    test_issue61
    ~~~~~~~~~~~~

    Test multiple keys in a single cite.
"""

import common
import pytest


@pytest.mark.sphinx('html', testroot='issue61')
def test_multiple_keys(app, warning):
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text()
    cits = {match.group('label')
            for match in common.html_citations().finditer(output)}
    citrefs = {match.group('label')
               for match in common.html_citation_refs().finditer(output)}
    assert {"App", "Bra"} == cits == citrefs
