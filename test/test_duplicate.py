"""Test warnings on duplicate labels/keys."""

from test.common import html_citation_refs, html_citations

import pytest


@pytest.mark.sphinx("html", testroot="duplicate_label")
def test_duplicate_label(app, warning) -> None:
    # see github issue 14
    app.build()
    assert 'duplicate label "1" for keys "Test" and "Test2"' in warning.getvalue()
    output = (app.outdir / "doc1.html").read_text()
    output2 = (app.outdir / "doc2.html").read_text()
    assert html_citations(label="1").search(output)
    assert html_citations(label="1").search(output2)


@pytest.mark.sphinx("html", testroot="duplicate_citation")
def test_duplicate_citation(app, warning) -> None:
    app.build()
    warning.seek(0)
    warnings = list(warning.readlines())
    assert len(warnings) == 1
    assert 'duplicate citation for key "Test"' in warnings[0]
    # assure distinct citation ids
    output = (app.outdir / "index.html").read_text()
    ids = [match.group("id_") for match in html_citations().finditer(output)]
    assert len(ids) == 2  # just to check ids are found
    assert len(set(ids)) == 2, "citation ids not unique"


@pytest.mark.sphinx("html", testroot="duplicate_nearly_identical_entries")
def test_duplicate_nearly_identical_entries(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text()
    cits = list(html_citations().finditer(output))
    cit_refs = list(html_citation_refs().finditer(output))
    assert len(cits) == len(cit_refs) == 2
    assert (
        {cit.group("label") for cit in cits}
        == {cit_ref.group("label") for cit_ref in cit_refs}
        == {"xyz19a", "xyz19b"}
    )


@pytest.mark.sphinx("html", testroot="duplicate_nearly_identical_keys", freshenv=True)
def test_duplicate_nearly_identical_keys_1(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text()
    # assure both citations and citation references are present
    assert html_citation_refs(label="Smi").search(output)
    assert html_citation_refs(label="Pop").search(output)
    assert html_citation_refs(label="Ein").search(output)
    assert html_citations(label="Smi").search(output)
    assert html_citations(label="Pop").search(output)
    assert html_citations(label="Ein").search(output)
    # assure distinct ids for citations
    ids = {match.group("id_") for match in html_citations().finditer(output)}
    refids = {match.group("refid") for match in html_citation_refs().finditer(output)}
    assert None not in ids
    assert len(ids) == 3
    assert ids == refids


@pytest.mark.sphinx(
    "html",
    testroot="duplicate_nearly_identical_keys",
    freshenv=True,
    confoverrides={"bibtex_cite_id": "cite-{bibliography_count}-{key}"},
)
def test_duplicate_nearly_identical_keys_2(app, warning) -> None:
    app.build()
    warning.seek(0)
    warnings = list(warning.readlines())
    assert len(warnings) == 2
    assert "duplicate citation id cite-1-test" in warnings[0]
    assert "duplicate citation id cite-1-test" in warnings[1]
    output = (app.outdir / "index.html").read_text()
    # assure both citations and citation references are present
    assert html_citation_refs(label="Smi").search(output)
    assert html_citation_refs(label="Pop").search(output)
    assert html_citation_refs(label="Ein").search(output)
    assert html_citations(label="Smi").search(output)
    assert html_citations(label="Pop").search(output)
    assert html_citations(label="Ein").search(output)
    # assure distinct ids for citations
    ids = {match.group("id_") for match in html_citations().finditer(output)}
    refids = {match.group("refid") for match in html_citation_refs().finditer(output)}
    assert None not in ids
    assert len(ids) == 3
    assert ids == refids


# this test "accidentally" includes a user provided id which
# clashes with a bibtex generated citation id
@pytest.mark.sphinx("html", testroot="duplicate_citation_id")
def test_duplicate_citation_id(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text()
    user_ids = {"id1", "id2", "id3"}
    ids = {match.group("id_") for match in html_citations().finditer(output)}
    refids = {match.group("refid") for match in html_citation_refs().finditer(output)}
    assert ids == refids
    assert len(ids) == 1
    assert not (user_ids & ids)
