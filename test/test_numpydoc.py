from test.common import (
    html_citation_refs_single,
    html_citations,
    html_footnote_refs,
    html_footnotes,
)

import pytest


@pytest.mark.numpydoc
@pytest.mark.sphinx(
    "html",
    testroot="autodoc",
    confoverrides={
        "extensions": ["sphinxcontrib.bibtex", "numpydoc"],
        "numpydoc_class_members_toctree": False,
    },
)
def test_numpydoc(app, warning) -> None:
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
