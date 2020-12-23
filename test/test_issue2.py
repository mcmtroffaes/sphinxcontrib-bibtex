# -*- coding: utf-8 -*-
"""
    test_issue2
    ~~~~~~~~~~~

    Test mixing of ``:cite:`` and ``[]_``.
"""

from typing import cast
import pytest

from sphinxcontrib.bibtex.cache import BibtexDomain


@pytest.mark.sphinx('html', testroot='issue2')
def test_mixing_citation_styles(app, warning):
    app.build()
    assert not warning.getvalue()
    domain = cast(BibtexDomain, app.env.get_domain('cite'))
    assert len(domain.citation_refs) == 1
    citation_ref = domain.citation_refs.pop()
    assert citation_ref.key == 'Test'
    assert citation_ref.docname == 'adoc1'
    assert len(domain.citations) == 1
    citation = domain.citations.pop()
    assert citation.entry_label == '1'
