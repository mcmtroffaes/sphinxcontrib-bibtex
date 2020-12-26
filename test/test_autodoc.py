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
    for id_ in ids:
        id2 = 'bibtex-citation-%s' % id_
        assert len(common.html_citation_refs(refid=id2).findall(output)) == 1
        assert len(common.html_citations(id_=id2).findall(output)) == 1
    output2 = (app.outdir / "doc_footcite.html").read_text()
    for id_ in ids:
        assert len(common.html_footnote_refs(refid=id_).findall(output2)) == 1
        assert len(common.html_footnotes(id_=id_).findall(output2)) == 1
