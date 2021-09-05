from typing import Set

from test.common import \
    html_citations, html_citation_refs, html_footnotes, html_footnote_refs
import pytest
import re


def citation_refs(output) -> Set[str]:
    return {match.group('label')
            for match in html_citation_refs().finditer(output)}


def citations(output) -> Set[str]:
    return {match.group('label')
            for match in html_citations().finditer(output)}


@pytest.mark.sphinx('html', testroot='bibliography_empty', freshenv=True)
def test_bibliography_empty(app, warning) -> None:
    app.build()
    assert not warning.getvalue()


@pytest.mark.sphinx('html', testroot='bibliography_header')
def test_bibliography_header(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text(encoding='utf-8')
    assert 'Regular Citations' in output
    assert 'Footnote Citations' in output


@pytest.mark.sphinx(
    'pseudoxml', testroot='bibliography_empty', freshenv=True, confoverrides={
        'bibtex_bibliography_header': '.. rubric:: Regular Citations',
        'bibtex_footbibliography_header': '.. rubric:: Footnote Citations'})
def test_bibliography_empty_no_header(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.pseudoxml").read_text(encoding='utf-8')
    assert 'Regular Citations' not in output
    assert 'Footnote Citations' not in output
    assert '<rubric' not in output


@pytest.mark.sphinx('html', testroot='bibliography_style_default')
def test_bibliography_style_default(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text()
    # ensure Man09 is cited with plain style and not with alpha style
    assert citation_refs(output) == citations(output) == {"1"}


@pytest.mark.sphinx('html', testroot='bibliography_style_label_1')
def test_bibliography_style_label_1(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text()
    # the custom style uses keys as labels
    # citations
    assert len(html_citations(
        label='myfancybibtexkey').findall(output)) == 1
    assert len(html_citations(
        label='myotherfancybibtexkey').findall(output)) == 1
    assert len(html_citation_refs(
        label='myfancybibtexkey').findall(output)) == 1
    assert len(html_citation_refs(
        label='myotherfancybibtexkey').findall(output)) == 1


@pytest.mark.sphinx('html', testroot='bibliography_style_label_2')
def test_bibliography_style_label_2(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text()
    assert len(html_citation_refs(label='APAa').findall(output)) == 1
    assert len(html_citation_refs(label='APAb').findall(output)) == 1


@pytest.mark.sphinx('html', testroot='bibliography_style_nowebref')
def test_bibliography_style_nowebref(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text(encoding='utf-8')
    # the custom style suppresses web links
    assert 'http://arxiv.org' not in output
    assert 'http://dx.doi.org' not in output


@pytest.mark.sphinx('html', testroot='bibliography_bad_option')
def test_bibliography_bad_option(app, warning) -> None:
    app.build()
    assert 'unknown option: "thisisintentionallyinvalid"' in warning.getvalue()


# see issue 87
@pytest.mark.sphinx('html', testroot='bibliography_key_prefix')
def test_bibliography_key_prefix(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "doc0.html").read_text()
    assert citations(output) == citation_refs(output) == {'AMan09', 'AEve03'}
    output = (app.outdir / "doc1.html").read_text()
    assert citations(output) == citation_refs(output) == {'BMan09'}


@pytest.mark.sphinx('html', testroot='bibliography_label_prefix_1')
def test_bibliography_label_prefix_1(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "doc1.html").read_text()
    assert citations(output) == citation_refs(output) == {'A1'}
    output = (app.outdir / "doc2.html").read_text()
    assert citations(output) == citation_refs(output) == {'B1'}


@pytest.mark.sphinx('html', testroot='bibliography_label_prefix_2')
def test_bibliography_label_prefix_2(app, warning) -> None:
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
    # use <= instead of == as there are some extra reference nodes
    assert doc1_refs <= citation_refs(output1)
    assert doc1_cites == citations(output1)
    output2 = (app.outdir / "doc2.html").read_text()
    assert doc2_refs <= citation_refs(output2)
    assert doc2_cites == citations(output2)
    output3 = (app.outdir / "summary.html").read_text()
    assert sum_refs <= citation_refs(output3)
    assert sum_cites == citations(output3)
    # check citation reference from summary to doc1
    match1 = html_citations(label='AFM12').search(output1)
    match3 = html_citation_refs(label='AFM12').search(output3)
    assert match1
    assert match3
    assert match1.group('id_') == match3.group('refid')
    assert match3.group('refdoc') == 'doc1.html'


# test order of bibliography entries when using an unsorted style
@pytest.mark.sphinx('html', testroot='bibliography_order_unsorted')
def test_bibliography_order_unsorted(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text()
    assert re.search(
        '<dd>.*Test 1.*</dd>.*<dd>.*Test 2.*</dd>',
        output, re.DOTALL)


# see issue 187
@pytest.mark.sphinx('html', testroot='bibliography_multi_foot')
def test_bibliography_multi_foot(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text(encoding='utf-8')
    assert output.count('<p class="rubric"') == 3
    assert len(re.findall(
        html_footnotes(id_="footcite-2009-mandel"), output)) == 1
    assert len(re.findall(
        html_footnotes(id_="footcite-2003-evensen"), output)) == 1
    assert len(re.findall(
        html_footnotes(id_="footcite-1986-lorenc"), output)) == 1
    assert len(re.findall(
        html_footnote_refs(refid='footcite-2009-mandel'), output)) == 2
    assert len(re.findall(
        html_footnote_refs(refid='footcite-2003-evensen'), output)) == 1
    assert len(re.findall(
        html_footnote_refs(refid='footcite-1986-lorenc'), output)) == 1


@pytest.mark.sphinx('html', testroot='bibliography_missing_field')
def test_bibliography_missing_field(app, warning) -> None:
    app.build()
    assert 'missing year in testkey' in warning.getvalue()


@pytest.mark.sphinx('html', testroot='bibliography_content')
def test_bibliography_content(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output1 = (app.outdir / "doc1.html").read_text()
    output2 = (app.outdir / "doc2.html").read_text()
    output3 = (app.outdir / "doc3.html").read_text()
    assert citation_refs(output1) == {'One', 'Two'}
    assert citations(output1) == {'One', 'Two', 'Thr'}
    assert citation_refs(output2) == {'Fou', 'Fiv'}
    assert citations(output2) == {'Fiv', 'Six'}
    assert not citation_refs(output3)
    assert citations(output3) == {'Fou'}


@pytest.mark.sphinx('html', testroot='bibliography_bad_key')
def test_bibliography_bad_key(app, warning) -> None:
    app.build()
    assert 'could not find bibtex key "badkey"' in warning.getvalue()


def url(link: str) -> str:
    return f'<a class="reference external" href="{link}">{link}</a>'


@pytest.mark.sphinx('html', testroot='bibliography_url')
def test_bibliography_url(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text(encoding='utf-8')
    match1 = html_citations(label='Een').search(output)
    match2 = html_citations(label='Twe').search(output)
    match3 = html_citations(label='Dri').search(output)
    match4 = html_citations(label='Vie').search(output)
    assert match1 is not None
    assert match2 is not None
    assert match3 is not None
    assert match4 is not None
    assert url('https://github.com/') in match1.group('text')
    assert 'aaa' + url('https://google.com/') + 'bbb' in match2.group('text')
    assert url('https://youtube.com/') in match3.group('text')
    assert 'URL: ' + url('https://wikipedia.org/') in match4.group('text')


@pytest.mark.sphinx('html', testroot='bibliography_custom_ids')
def test_bibliography_custom_ids(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text(encoding='utf-8')
    assert '<p id="bibliography-id-1">' in output
    assert '<p id="bibliography-id-2">' in output
    assert '<p id="footbibliography-id-1">' in output
    assert '<p id="footbibliography-id-2">' in output
    match1 = html_citations(text='.*Evensen.*').search(output)
    match2 = html_citations(text='.*Mandel.*').search(output)
    match3 = html_citations(text='.*Lorenc.*').search(output)
    assert match1 is not None
    assert match2 is not None
    assert match3 is not None
    assert match1.group('id_') == 'cite-id-1-2003-evensen'
    assert match2.group('id_') == 'cite-id-1-2009-mandel'
    assert match3.group('id_') == 'cite-id-2-1986-lorenc'
    match1 = html_footnotes(text='.*Evensen.*').search(output)
    match2 = html_footnotes(text='.*Mandel.*').search(output)
    match3 = html_footnotes(text='.*Lorenc.*').search(output)
    assert match1 is not None
    assert match2 is not None
    assert match3 is not None
    assert match1.group('id_') == 'footcite-id-2003-evensen'
    assert match2.group('id_') == 'footcite-id-2009-mandel'
    assert match3.group('id_') == 'footcite-id-1986-lorenc'
