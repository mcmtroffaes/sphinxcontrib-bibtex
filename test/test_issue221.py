"""
    test_issue221
    ~~~~~~~~~~~~~

    Test missing bibliography_key issue.
"""

import common
import pytest


@pytest.mark.sphinx('latex', testroot='issue221')
def test_issue221(app, warning):
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "python.tex").read_text()
    cits = common.latex_citations().finditer(output)
    cit_refs = common.latex_citation_refs().finditer(output)
    assert [cit.group('docname') for cit in cits] == ['sources']
    assert [cit_ref.group('docname') for cit_ref in cit_refs] == ['sources']
    assert ([cit.group('id_') for cit in cits] ==
            [cit.group('refid') for cit in cit_refs])
