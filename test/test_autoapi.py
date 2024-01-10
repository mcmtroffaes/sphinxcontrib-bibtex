"""
    test_autodoc
    ~~~~~~~~~~~~

    Test with autodoc.
"""

import sphinx

from test.common import (
    html_citation_refs_single,
    html_citations,
    html_footnote_refs,
    html_footnotes,
)

import pytest


@pytest.mark.skipif(
    sphinx.version_info < (7, 0),
    reason="autoapi appears broken on sphinx < 7.0",
)
@pytest.mark.sphinx("html", testroot="autoapi")
def test_autoapi(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    root = (app.outdir / "index.html").read_text()
    output = (app.outdir / "autoapi/some_module/cite/index.html").read_text()
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
        assert len(html_citations(label=label).findall(root)) == 1
        match_ref = html_citation_refs_single(label=label).search(output)
        match = html_citations(label=label).search(root)
        assert match_ref
        assert match
        assert match_ref.group("refid") == match.group("id_")
        assert title in match.group("text")
        # no backrefs as citations are in other document
        # assert match_ref.group("id_") == match.group("backref")
    output2 = (app.outdir / "autoapi/some_module/footcite/index.html").read_text()
    assert len(html_footnote_refs().findall(output2)) == 11
    for title in titles:
        text = ".*" + title + ".*"
        assert len(html_footnotes(text=text).findall(output2)) == 1
        match = html_footnotes(text=text).search(output2)
        assert match
        id_ = match.group("id_")
        assert len(html_footnote_refs(refid=id_).findall(output2)) == 1
