from test.common import latex_citation_refs, latex_citations

import pytest


@pytest.mark.sphinx("latex", testroot="latex_refs")
def test_latex_refs(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "test.tex").read_text(encoding="utf-8-sig")
    assert len(latex_citations().findall(output)) == 1
    assert len(latex_citation_refs().findall(output)) == 1
    match = latex_citations().search(output)
    match_ref = latex_citation_refs().search(output)
    assert match.group("label") == "Huy57"
    assert match.group("docname") == "index"
    assert "De ratiociniis in ludo aleæ." in match.group("text")
    assert match_ref.group("refid") == match.group("id_")
    assert match_ref.group("docname") == "index"


@pytest.mark.sphinx("latex", testroot="latex_multidoc")
def test_latex_multidoc(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "test.tex").read_text(encoding="utf-8-sig")
    assert len(latex_citations().findall(output)) == 1
    assert len(latex_citation_refs().findall(output)) == 1
    match = latex_citations().search(output)
    match_ref = latex_citation_refs().search(output)
    assert match.group("docname") == match_ref.group("docname") == "sources"
    assert match.group("id_") is not None
    assert match_ref.group("refid") == match.group("id_")


@pytest.mark.sphinx("latex", testroot="latex_multidoc_2")
def test_latex_multidoc_2(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "test.tex").read_text(encoding="utf-8-sig")
    assert len(latex_citations().findall(output)) == 1
    assert len(latex_citation_refs().findall(output)) == 1
    match = latex_citations().search(output)
    match_ref = latex_citation_refs().search(output)
    assert match.group("docname") == match_ref.group("docname") == "sources"
    assert match.group("id_") is not None
    assert match_ref.group("refid") == match.group("id_")
