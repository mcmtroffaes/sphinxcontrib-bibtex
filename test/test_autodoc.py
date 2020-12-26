"""
    test_autodoc
    ~~~~~~~~~~~~

    Test with autodoc.
"""

import common
import pytest


@pytest.mark.sphinx('html', testroot='autodoc')
def test_autodoc(app, warning):
    app.builder.build_all()
    assert not warning.getvalue()
    output = (app.outdir / "doc_cite.html").read_text()
    names = ['testmodule', 'testfunc', 'testfuncarg', 'testdata', 'testclass',
             'testclassattr', 'testinstanceattr', 'testinit', 'testinitarg',
             'testmethod', 'testmethodarg']
    for name in names:
        assert len(common.html_citation_refs(name=name).findall(output)) == 1
        assert len(common.html_citations(name=name).findall(output)) == 1
    output2 = (app.outdir / "doc_footcite.html").read_text()
    for name in names:
        assert len(common.html_footnote_refs(name=name).findall(output2)) == 1
        assert len(common.html_footnotes(name=name).findall(output2)) == 1
