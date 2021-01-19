"""
    test_autodoc
    ~~~~~~~~~~~~

    Test with autodoc.
"""

import common
import pytest


@pytest.mark.sphinx('html', testroot='autodoc')
def test_autodoc(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "doc_cite.html").read_text()
    labels = ['One', 'Two', 'Thr', 'Fou', 'Fiv', 'Six', 'Sev', 'Eig', 'Nin',
              'Ten', 'Ele']
    titles = ['Een', 'Twee', 'Drie', 'Vier', 'Vijf', 'Zes', 'Zeven', 'Acht',
              'Negen', 'Tien', 'Elf']
    for label, title in zip(labels, titles):
        assert len(common.html_citation_refs(label=label).findall(output)) == 1
        assert len(common.html_citations(label=label).findall(output)) == 1
        match_ref = common.html_citation_refs(label=label).search(output)
        match = common.html_citations(label=label).search(output)
        assert match_ref
        assert match
        assert match_ref.group('refid') == match.group('id_')
        assert title in match.group('text')
    output2 = (app.outdir / "doc_footcite.html").read_text()
    assert len(common.html_footnote_refs().findall(output2)) == 11
    for title in titles:
        text = ".*" + title + ".*"
        assert len(common.html_footnotes(text=text).findall(output2)) == 1
        match = common.html_footnotes(text=text).search(output2)
        assert match
        id_ = match.group('id_')
        assert len(common.html_footnote_refs(refid=id_).findall(output2)) == 1


# test that sphinx [source] links do not generate a warning (issue 17)
@pytest.mark.sphinx('html', testroot='autodoc_viewcode')
def test_autodoc_viewcode(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
