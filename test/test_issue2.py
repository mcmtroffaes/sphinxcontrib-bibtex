# -*- coding: utf-8 -*-
"""
    test_issue2
    ~~~~~~~~~~~

    Test mixing of ``:cite:`` and ``[]_``.
"""

import pytest


@pytest.mark.sphinx('html', testroot='issue2')
def test_mixing_citation_styles(app, warning):
    app.builder.build_all()
    assert not warning.getvalue()
    cited_docnames = [
        docname for docname, keys in app.env.bibtex_cache.cited.items()
        if u"Test" in keys]
    assert cited_docnames == [u"adoc1"]
    assert app.env.bibtex_cache.get_label_from_key(u"Test") == u"1"
