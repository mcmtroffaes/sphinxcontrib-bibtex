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
    ids = ['testmodule', 'testfunc', 'testfuncarg', 'testdata', 'testclass',
           'testclassattr', 'testinstanceattr', 'testinit', 'testinitarg',
           'testmethod', 'testmethodarg']
    for name in ids:
        assert len(common.html_citation_refs(name=name).findall(output)) == 1
        assert len(common.html_citations(name=name).findall(output)) == 1
    output2 = (app.outdir / "doc_footcite.html").read_text()
    for id_ in ids:
        assert len(common.html_footnote_refs(refid=id_).findall(output2)) == 1
        assert len(common.html_footnotes(id_=id_).findall(output2)) == 1
