import common
import pytest


def get_citation_refs(code):
    return {match.group('label')
            for match in common.html_citation_refs().finditer(code)}


def get_citations(code):
    return {match.group('label')
            for match in common.html_citations().finditer(code)}


@pytest.mark.sphinx('html', testroot='label_prefix_1')
def test_label_prefix_1(app, warning):
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "doc1.html").read_text()
    assert get_citations(output) == get_citation_refs(output) == {'A1'}
    output = (app.outdir / "doc2.html").read_text()
    assert get_citations(output) == get_citation_refs(output) == {'B1'}


@pytest.mark.sphinx('html', testroot='label_prefix_2')
def test_label_prefix_2(app, warning):
    doc1_refs = {'AFM12', 'ABlu83', 'AGIH02', 'AWS14'}
    doc1_cites = {'ABlu83', 'AFM12', 'AGIH02', 'AWS14'}
    doc2_refs = {'BShi13'}
    doc2_cites = {'BShi13'}
    sum_refs = {'CMcMahonKM10', 'CRMM11', 'CRM09', 'CMM03', 'CHdJMD13',
                'AFM12'}
    sum_cites = {'CMcMahonKM10', 'CRMM11', 'CRM09', 'CMM03', 'CHdJMD13'}
    app.build()
    assert not warning.getvalue()
    output1 = (app.outdir / "doc1.html").read_text()
    assert doc1_refs == get_citation_refs(output1)
    assert doc1_cites == get_citations(output1)
    output2 = (app.outdir / "doc2.html").read_text()
    assert doc2_refs == get_citation_refs(output2)
    assert doc2_cites == get_citations(output2)
    output3 = (app.outdir / "summary.html").read_text()
    assert sum_refs == get_citation_refs(output3)
    assert sum_cites == get_citations(output3)
    # check citation reference from summary to doc1
    match1 = common.html_citations(label='AFM12').search(output1)
    match3 = common.html_citation_refs(label='AFM12').search(output3)
    assert match1
    assert match3
    assert match1.group('id_') == match3.group('refid')
    assert match3.group('refdoc') == 'doc1.html'
