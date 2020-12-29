import common
import pytest


@pytest.mark.sphinx('latex', testroot='latex_refs')
def test_latex_refs(app, warning):
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "test.tex").read_text()
    assert len(common.latex_citations().findall(output)) == 1
    assert len(common.latex_citation_refs().findall(output)) == 1
    match = common.latex_citations().search(output)
    match_ref = common.latex_citation_refs().search(output)
    assert match.group('label') == 'Huy57'
    assert match.group('docname') == 'index'
    assert "De ratiociniis in ludo aleæ." in match.group('text')
    assert match_ref.group('refid') == match.group('id_')
    assert match_ref.group('docname') == 'index'


@pytest.mark.sphinx('latex', testroot='latex_multidoc')
def test_latex_multidoc(app, warning):
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "test.tex").read_text()
    cits = common.latex_citations().finditer(output)
    cit_refs = common.latex_citation_refs().finditer(output)
    assert [cit.group('docname') for cit in cits] == ['sources']
    assert [cit_ref.group('docname') for cit_ref in cit_refs] == ['sources']
    assert ([cit.group('id_') for cit in cits] ==
            [cit_ref.group('refid') for cit_ref in cit_refs])
