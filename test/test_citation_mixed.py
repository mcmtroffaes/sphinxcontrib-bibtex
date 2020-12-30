from typing import cast
import pytest

from sphinxcontrib.bibtex.domain import BibtexDomain


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
