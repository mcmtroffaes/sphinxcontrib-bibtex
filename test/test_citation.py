import common
import pytest

from sphinxcontrib.bibtex.domain import BibtexDomain
from typing import cast


@pytest.mark.sphinx('html', testroot='citation_not_found')
def test_citation_not_found(app, warning):
    app.build()
    assert 'could not find bibtex key "nosuchkey1"' in warning.getvalue()
    assert 'could not find bibtex key "nosuchkey2"' in warning.getvalue()


# test mixing of ``:cite:`` and ``[]_`` (issue 2)
@pytest.mark.sphinx('html', testroot='citation_mixed')
def test_citation_mixed(app, warning):
    app.build()
    assert not warning.getvalue()
    domain = cast(BibtexDomain, app.env.get_domain('cite'))
    assert len(domain.citation_refs) == 1
    citation_ref = domain.citation_refs.pop()
    assert citation_ref.keys == ['Test']
    assert citation_ref.docname == 'adoc1'
    assert len(domain.citations) == 1
    citation = domain.citations.pop()
    assert citation.formatted_entry.label == '1'


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


# see issue 85
@pytest.mark.sphinx('html', testroot='citation_no_author_no_key')
def test_citation_no_author_no_key(app, warning):
    app.build()
    assert not warning.getvalue()


# test cites spanning multiple lines (issue 205)
@pytest.mark.sphinx('html', testroot='citation_whitespace')
def test_citation_whitespace(app, warning):
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text()
    # ensure Man09 is cited
    assert len(common.html_citation_refs(label='Fir').findall(output)) == 1
    assert len(common.html_citation_refs(label='Sec').findall(output)) == 1


# test document not in toctree (issue 228)
@pytest.mark.sphinx('pseudoxml', testroot='citation_from_orphan')
def test_citation_from_orphan(app, warning):
    app.build()
    assert not warning.getvalue()
