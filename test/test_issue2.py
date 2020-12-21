# -*- coding: utf-8 -*-
"""
    test_issue2
    ~~~~~~~~~~~

    Test mixing of ``:cite:`` and ``[]_``.
"""

from typing import cast
import pytest

from sphinxcontrib.bibtex.cache import BibtexCitationDomain


@pytest.mark.sphinx('html', testroot='issue2')
def test_mixing_citation_styles(app, warning):
    app.build()
    assert not warning.getvalue()
    domain = cast(BibtexCitationDomain, app.env.get_domain('cite'))
    cited_docnames = [
        docname for docname, keys in domain.cited.items()
        if u"Test" in keys]
    assert cited_docnames == [u"adoc1"]
    assert domain.get_label_from_key(u"Test") == u"1"
