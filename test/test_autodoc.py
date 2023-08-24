"""
    test_autodoc
    ~~~~~~~~~~~~

    Test with autodoc.
"""

import test.some_module.cite
import test.some_module.footcite
from test.common import (
    html_citation_refs_single,
    html_citations,
    html_footnote_refs,
    html_footnotes,
)

import pytest


# for coverage
def test_some_module() -> None:
    f1 = test.some_module.cite.Foo(0)
    assert f1.c == 3
    f2 = test.some_module.footcite.Foo(0)
    assert f2.c == 3


@pytest.mark.sphinx("html", testroot="autodoc")
def test_autodoc(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "doc_cite.html").read_text()
    labels = [
        "One",
        "Two",
        "Thr",
        "Fou",
        "Fiv",
        "Six",
        "Sev",
        "Eig",
        "Nin",
        "Ten",
        "Ele",
    ]
    titles = [
        "Een",
        "Twee",
        "Drie",
        "Vier",
        "Vijf",
        "Zes",
        "Zeven",
        "Acht",
        "Negen",
        "Tien",
        "Elf",
    ]
    for label, title in zip(labels, titles):
        assert len(html_citation_refs_single(label=label).findall(output)) == 1
        assert len(html_citations(label=label).findall(output)) == 1
        match_ref = html_citation_refs_single(label=label).search(output)
        match = html_citations(label=label).search(output)
        assert match_ref
        assert match
        assert match_ref.group("refid") == match.group("id_")
        assert title in match.group("text")
        assert match_ref.group("id_") == match.group("backref")
    output2 = (app.outdir / "doc_footcite.html").read_text()
    assert len(html_footnote_refs().findall(output2)) == 11
    for title in titles:
        text = ".*" + title + ".*"
        assert len(html_footnotes(text=text).findall(output2)) == 1
        match = html_footnotes(text=text).search(output2)
        assert match
        id_ = match.group("id_")
        assert len(html_footnote_refs(refid=id_).findall(output2)) == 1


# test that sphinx [source] links do not generate a warning (issue 17)
@pytest.mark.sphinx("html", testroot="autodoc_viewcode")
def test_autodoc_viewcode(app, warning) -> None:
    app.build()
    assert not warning.getvalue()


@pytest.mark.cython
@pytest.mark.sphinx("html", testroot="autodoc_cython")
def test_autodoc_cython(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "doc_cite.html").read_text()
    labels = [
        "One",
        "Two",
        "Thr",
        # 'Fou',
        "Fiv",
        # 'Six', 'Sev',
        "Eig",
        "Nin",
        "Ten",
        "Ele",
    ]
    titles = [
        "Een",
        "Twee",
        "Drie",
        # 'Vier',
        "Vijf",
        # 'Zes', 'Zeven',
        "Acht",
        "Negen",
        "Tien",
        "Elf",
    ]
    for label, title in zip(labels, titles):
        assert len(html_citation_refs_single(label=label).findall(output)) == 1
        assert len(html_citations(label=label).findall(output)) == 1
        match_ref = html_citation_refs_single(label=label).search(output)
        match = html_citations(label=label).search(output)
        assert match_ref
        assert match
        assert match_ref.group("refid") == match.group("id_")
        assert title in match.group("text")
        assert match_ref.group("id_") == match.group("backref")
    output2 = (app.outdir / "doc_footcite.html").read_text()
    assert len(html_footnote_refs().findall(output2)) == len(labels)
    for title in titles:
        text = ".*" + title + ".*"
        assert len(html_footnotes(text=text).findall(output2)) == 1
        match = html_footnotes(text=text).search(output2)
        assert match
        id_ = match.group("id_")
        assert len(html_footnote_refs(refid=id_).findall(output2)) == 1
