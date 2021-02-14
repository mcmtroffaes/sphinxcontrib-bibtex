from typing import Set

import common
import pytest
import re


def citation_refs(output) -> Set[str]:
    return {match.group('label')
            for match in common.html_citation_refs().finditer(output)}


def citations(output) -> Set[str]:
    return {match.group('label')
            for match in common.html_citations().finditer(output)}


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
    assert len(common.html_citations(
        label='myfancybibtexkey').findall(output)) == 1
    assert len(common.html_citations(
        label='myotherfancybibtexkey').findall(output)) == 1
    assert len(common.html_citation_refs(
        label='myfancybibtexkey').findall(output)) == 1
    assert len(common.html_citation_refs(
        label='myotherfancybibtexkey').findall(output)) == 1


@pytest.mark.sphinx('html', testroot='bibliography_style_label_2')
def test_bibliography_style_label_2(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text()
    assert len(common.html_citation_refs(label='APAa').findall(output)) == 1
    assert len(common.html_citation_refs(label='APAb').findall(output)) == 1


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
    match1 = common.html_citations(label='AFM12').search(output1)
    match3 = common.html_citation_refs(label='AFM12').search(output3)
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
    assert len(re.findall('id="mandel"', output)) == 1
    assert len(re.findall('id="evensen"', output)) == 1
    assert len(re.findall('id="lorenc"', output)) == 1
    assert len(re.findall(
        'class="footnote-reference brackets" href="#mandel"', output)) == 2
    assert len(re.findall(
        'class="footnote-reference brackets" href="#evensen"', output)) == 1
    assert len(re.findall(
        'class="footnote-reference brackets" href="#lorenc"', output)) == 1


@pytest.mark.sphinx('html', testroot='bibliography_missing_field')
def test_bibliography_missing_field(app, warning) -> None:
    app.build()
    assert 'missing year in testkey' in warning.getvalue()
