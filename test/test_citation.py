import re
from dataclasses import dataclass, field
from test.common import html_citation_refs, html_citations, html_docutils_citation_refs
from typing import cast

import pybtex.plugin
import pytest
from pybtex.style.formatting.unsrt import Style as UnsrtStyle
from pybtex.style.template import words

import sphinxcontrib.bibtex.plugin
from sphinxcontrib.bibtex.domain import BibtexDomain
from sphinxcontrib.bibtex.style.referencing import BracketStyle, PersonStyle
from sphinxcontrib.bibtex.style.referencing.author_year import AuthorYearReferenceStyle


@pytest.mark.sphinx("html", testroot="citation_not_found")
def test_citation_not_found(app, warning) -> None:
    app.build()
    assert 'could not find bibtex key "nosuchkey1"' in warning.getvalue()
    assert 'could not find bibtex key "nosuchkey2"' in warning.getvalue()


# test mixing of ``:cite:`` and ``[]_`` (issue 2)
@pytest.mark.sphinx("html", testroot="citation_mixed")
def test_citation_mixed(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    domain = cast(BibtexDomain, app.env.get_domain("cite"))
    assert len(domain.citation_refs) == 1
    citation_ref = domain.citation_refs.pop()
    assert citation_ref.targets == [("Test", "", "")]
    assert citation_ref.docname == "adoc1"
    assert len(domain.citations) == 1
    citation = domain.citations.pop()
    assert citation.formatted_entry.label == "1"


@pytest.mark.sphinx("html", testroot="citation_multiple_keys")
def test_citation_multiple_keys(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text(encoding="utf-8-sig")
    cits = {match.group("label") for match in html_citations().finditer(output)}
    citrefs = {match.group("label") for match in html_citation_refs().finditer(output)}
    assert {"App", "Bra"} == cits == citrefs


@pytest.mark.sphinx("html", testroot="citation_any_role")
def test_citation_any_role(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text(encoding="utf-8-sig")
    cits = {match.group("label") for match in html_citations().finditer(output)}
    citrefs = {match.group("label") for match in html_citation_refs().finditer(output)}
    assert {"App", "Bra"} == cits == citrefs


def find_label(output: str, label: str):
    assert html_citation_refs(label=label).search(output) is not None


# see issue 85
@pytest.mark.sphinx("html", testroot="citation_no_author_no_key")
def test_citation_no_author_no_key(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text(encoding="utf-8-sig")
    find_label(output, "<em>Software projects built on Mesos</em>, 2015")
    find_label(output, "2015")
    find_label(output, "Mandel, 2009")
    find_label(output, "2009")
    find_label(output, "<em>This citation only has a title</em>, n.d.")
    find_label(output, "n.d.")
    find_label(output, "Whatever, 2021")
    find_label(output, "2021")


# test cites spanning multiple lines (issue 205)
@pytest.mark.sphinx("html", testroot="citation_whitespace")
def test_citation_whitespace(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text(encoding="utf-8-sig")
    # ensure Man09 is cited
    assert len(html_citation_refs(label="Fir").findall(output)) == 1
    assert len(html_citation_refs(label="Sec").findall(output)) == 1


# test document not in toctree (issue 228)
@pytest.mark.sphinx("pseudoxml", testroot="citation_from_orphan")
def test_citation_from_orphan(app, warning) -> None:
    app.build()
    assert not warning.getvalue()


@pytest.mark.sphinx("text", testroot="citation_roles")
def test_citation_roles_label(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.txt").read_text(encoding="utf-8-sig")
    tests = [
        ("p", " [dDEF03] "),
        ("ps", " [dDEF03] "),
        ("t", " de Du *et al.* [dDEF03] "),
        ("ts", " de Du, Em, and Fa [dDEF03] "),
        ("ct", " De Du *et al.* [dDEF03] "),
        ("cts", " De Du, Em, and Fa [dDEF03] "),
        ("labelpar", " [dDEF03] "),
        ("label", " dDEF03 "),
        ("yearpar", " [2003] "),
        ("year", " 2003 "),
        ("authorpar", " [de Du *et al.*] "),
        ("authorpars", " [de Du, Em, and Fa] "),
        ("author", " de Du *et al.* "),
        ("authors", " de Du, Em, and Fa "),
        ("cauthor", " De Du *et al.* "),
        ("cauthors", " De Du, Em, and Fa "),
        ("empty", " AAA  AAA "),
        ("p", " [aA01, BC02] "),
        ("ps", " [aA01, BC02] "),
        ("t", " al Ap [aA01], Be and Ci [BC02] "),
        ("ts", " al Ap [aA01], Be and Ci [BC02] "),
        ("ct", " Al Ap [aA01], Be and Ci [BC02] "),
        ("cts", " Al Ap [aA01], Be and Ci [BC02] "),
        ("labelpar", " [aA01, BC02] "),
        ("label", " aA01, BC02 "),
        ("yearpar", " [2001, 2002] "),
        ("year", " 2001, 2002 "),
        ("authorpar", " [al Ap, Be and Ci] "),
        ("authorpars", " [al Ap, Be and Ci] "),
        ("author", " al Ap, Be and Ci "),
        ("authors", " al Ap, Be and Ci "),
        ("cauthor", " Al Ap, Be and Ci "),
        ("cauthors", " Al Ap, Be and Ci "),
        ("empty", " BBB  BBB "),
        ("p", " [Ge04, Hu05, Ix06] "),
        ("ps", " [Ge04, Hu05, Ix06] "),
        ("t", " Ge [Ge04], Hu [Hu05], Ix [Ix06] "),
        ("ts", " Ge [Ge04], Hu [Hu05], Ix [Ix06] "),
        ("ct", " Ge [Ge04], Hu [Hu05], Ix [Ix06] "),
        ("cts", " Ge [Ge04], Hu [Hu05], Ix [Ix06] "),
        ("labelpar", " [Ge04, Hu05, Ix06] "),
        ("label", " Ge04, Hu05, Ix06 "),
        ("yearpar", " [2004, 2005, 2006] "),
        ("year", " 2004, 2005, 2006 "),
        ("authorpar", " [Ge, Hu, Ix] "),
        ("authorpars", " [Ge, Hu, Ix] "),
        ("author", " Ge, Hu, Ix "),
        ("authors", " Ge, Hu, Ix "),
        ("cauthor", " Ge, Hu, Ix "),
        ("cauthors", " Ge, Hu, Ix "),
        ("empty", " CCC  CCC "),
    ]
    for role, text in tests:
        escaped_text = re.escape(text)
        pattern = f'":cite:{role}:".*{escaped_text}'
        assert re.search(pattern, output) is not None
    # check :cite:empty: generates citation
    assert "[Ju07] Jo Ju. Testseven. 2007." in output


@pytest.mark.sphinx(
    "text",
    testroot="citation_roles",
    confoverrides={"bibtex_reference_style": "author_year"},
)
def test_citation_roles_authoryear(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.txt").read_text(encoding="utf-8-sig")
    tests = [
        ("p", " [de Du *et al.*, 2003] "),
        ("ps", " [de Du, Em, and Fa, 2003] "),
        ("alp", " de Du *et al.*, 2003 "),
        ("alps", " de Du, Em, and Fa, 2003 "),
        ("t", " de Du *et al.* [2003] "),
        ("ts", " de Du, Em, and Fa [2003] "),
        ("ct", " De Du *et al.* [2003] "),
        ("cts", " De Du, Em, and Fa [2003] "),
        ("labelpar", " [dDEF03] "),
        ("label", " dDEF03 "),
        ("yearpar", " [2003] "),
        ("year", " 2003 "),
        ("authorpar", " [de Du *et al.*] "),
        ("authorpars", " [de Du, Em, and Fa] "),
        ("author", " de Du *et al.* "),
        ("authors", " de Du, Em, and Fa "),
        ("cauthor", " De Du *et al.* "),
        ("cauthors", " De Du, Em, and Fa "),
        ("empty", " AAA  AAA "),
        ("p", " [al Ap, 2001, Be and Ci, 2002] "),
        ("ps", " [al Ap, 2001, Be and Ci, 2002] "),
        ("alp", " al Ap, 2001, Be and Ci, 2002 "),
        ("alps", " al Ap, 2001, Be and Ci, 2002 "),
        ("t", " al Ap [2001], Be and Ci [2002] "),
        ("ts", " al Ap [2001], Be and Ci [2002] "),
        ("ct", " Al Ap [2001], Be and Ci [2002] "),
        ("cts", " Al Ap [2001], Be and Ci [2002] "),
        ("labelpar", " [aA01, BC02] "),
        ("label", " aA01, BC02 "),
        ("yearpar", " [2001, 2002] "),
        ("year", " 2001, 2002 "),
        ("authorpar", " [al Ap, Be and Ci] "),
        ("authorpars", " [al Ap, Be and Ci] "),
        ("author", " al Ap, Be and Ci "),
        ("authors", " al Ap, Be and Ci "),
        ("cauthor", " Al Ap, Be and Ci "),
        ("cauthors", " Al Ap, Be and Ci "),
        ("empty", " BBB  BBB "),
        ("p", " [Ge, 2004, Hu, 2005, Ix, 2006] "),
        ("ps", " [Ge, 2004, Hu, 2005, Ix, 2006] "),
        ("alp", " Ge, 2004, Hu, 2005, Ix, 2006 "),
        ("alps", " Ge, 2004, Hu, 2005, Ix, 2006 "),
        ("t", " Ge [2004], Hu [2005], Ix [2006] "),
        ("ts", " Ge [2004], Hu [2005], Ix [2006] "),
        ("ct", " Ge [2004], Hu [2005], Ix [2006] "),
        ("cts", " Ge [2004], Hu [2005], Ix [2006] "),
        ("labelpar", " [Ge04, Hu05, Ix06] "),
        ("label", " Ge04, Hu05, Ix06 "),
        ("yearpar", " [2004, 2005, 2006] "),
        ("year", " 2004, 2005, 2006 "),
        ("authorpar", " [Ge, Hu, Ix] "),
        ("authorpars", " [Ge, Hu, Ix] "),
        ("author", " Ge, Hu, Ix "),
        ("authors", " Ge, Hu, Ix "),
        ("cauthor", " Ge, Hu, Ix "),
        ("cauthors", " Ge, Hu, Ix "),
        ("empty", " CCC  CCC "),
    ]
    for role, text in tests:
        escaped_text = re.escape(text)
        pattern = f'":cite:{role}:".*{escaped_text}'
        assert re.search(pattern, output) is not None
    # check :cite:empty: generates citation
    assert "[Ju07] Jo Ju. Testseven. 2007." in output


@pytest.mark.sphinx("text", testroot="citation_roles_pre_post")
def test_citation_roles_label_pre_post(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.txt").read_text(encoding="utf-8-sig")
    lab1 = "dDEF03"
    lab2 = "aA01"
    lab3 = "BC02"
    ref1 = "de Du *et al.*"
    ref2 = "al Ap"
    ref3 = "Be and Ci"
    tests = [
        ("p", f" A [see {lab1}] "),
        ("p", f" B [{lab1}, p. 1] "),
        ("p", f" C [see {lab1}, p. 1] "),
        ("t", f" A {ref1} [see {lab1}] "),
        ("t", f" B {ref1} [{lab1}, p. 1] "),
        ("t", f" C {ref1} [see {lab1}, p. 1] "),
        ("p", f" A [see {lab2}, {lab3}] "),
        ("p", f" B [{lab2}, p. 1, {lab3}] "),
        ("p", f" C [see {lab2}, p. 1, {lab3}] "),
        ("p", f" D [{lab2}, see {lab3}] "),
        ("p", f" E [{lab2}, {lab3}, p. 2] "),
        ("p", f" F [{lab2}, see {lab3}, p. 2] "),
        ("p", f" G [see {lab2}, see {lab3}] "),
        ("p", f" H [{lab2}, p. 1, {lab3}, p. 2] "),
        ("p", f" I [see {lab2}, {lab3}, p. 2] "),
        ("p", f" J [see {lab2}, p. 1, see {lab3}, p. 2] "),
        ("t", f" A {ref2} [see {lab2}], {ref3} [{lab3}] "),
        ("t", f" B {ref2} [{lab2}, p. 1], {ref3} [{lab3}] "),
        ("t", f" C {ref2} [see {lab2}, p. 1], {ref3} [{lab3}] "),
        ("t", f" D {ref2} [{lab2}], {ref3} [see {lab3}] "),
        ("t", f" E {ref2} [{lab2}], {ref3} [{lab3}, p. 2] "),
        ("t", f" F {ref2} [{lab2}], {ref3} [see {lab3}, p. 2] "),
        ("t", f" G {ref2} [see {lab2}], {ref3} [see {lab3}] "),
        ("t", f" H {ref2} [{lab2}, p. 1], {ref3} [{lab3}, p. 2] "),
        ("t", f" I {ref2} [see {lab2}], {ref3} [{lab3}, p. 2] "),
        ("t", f" J {ref2} [see {lab2}, p. 1], {ref3} [see {lab3}, p. 2] "),
    ]
    for role, text in tests:
        escaped_text = re.escape(text)
        pattern = f'":cite:{role}:".*{escaped_text}'
        assert re.search(pattern, output) is not None, text


@pytest.mark.sphinx(
    "text",
    testroot="citation_roles_pre_post",
    confoverrides={"bibtex_reference_style": "author_year"},
)
def test_citation_roles_authoryear_pre_post(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.txt").read_text(encoding="utf-8-sig")
    ref1 = "de Du *et al.*"
    ref2 = "al Ap"
    ref3 = "Be and Ci"
    tests = [
        ("p", f" A [see {ref1}, 2003] "),
        ("p", f" B [{ref1}, 2003, p. 1] "),
        ("p", f" C [see {ref1}, 2003, p. 1] "),
        ("t", f" A {ref1} [see 2003] "),
        ("t", f" B {ref1} [2003, p. 1] "),
        ("t", f" C {ref1} [see 2003, p. 1] "),
        ("p", f" A [see {ref2}, 2001, {ref3}, 2002] "),
        ("p", f" B [{ref2}, 2001, p. 1, {ref3}, 2002] "),
        ("p", f" C [see {ref2}, 2001, p. 1, {ref3}, 2002] "),
        ("p", f" D [{ref2}, 2001, see {ref3}, 2002] "),
        ("p", f" E [{ref2}, 2001, {ref3}, 2002, p. 2] "),
        ("p", f" F [{ref2}, 2001, see {ref3}, 2002, p. 2] "),
        ("p", f" G [see {ref2}, 2001, see {ref3}, 2002] "),
        ("p", f" H [{ref2}, 2001, p. 1, {ref3}, 2002, p. 2] "),
        ("p", f" I [see {ref2}, 2001, {ref3}, 2002, p. 2] "),
        ("p", f" J [see {ref2}, 2001, p. 1, see {ref3}, 2002, p. 2] "),
        ("t", f" A {ref2} [see 2001], {ref3} [2002] "),
        ("t", f" B {ref2} [2001, p. 1], {ref3} [2002] "),
        ("t", f" C {ref2} [see 2001, p. 1], {ref3} [2002] "),
        ("t", f" D {ref2} [2001], {ref3} [see 2002] "),
        ("t", f" E {ref2} [2001], {ref3} [2002, p. 2] "),
        ("t", f" F {ref2} [2001], {ref3} [see 2002, p. 2] "),
        ("t", f" G {ref2} [see 2001], {ref3} [see 2002] "),
        ("t", f" H {ref2} [2001, p. 1], {ref3} [2002, p. 2] "),
        ("t", f" I {ref2} [see 2001], {ref3} [2002, p. 2] "),
        ("t", f" J {ref2} [see 2001, p. 1], {ref3} [see 2002, p. 2] "),
    ]
    for role, text in tests:
        escaped_text = re.escape(text)
        pattern = f'":cite:{role}:".*{escaped_text}'
        assert re.search(pattern, output) is not None, text


@pytest.mark.sphinx(
    "html",
    testroot="citation_roles",
    confoverrides={"bibtex_default_style": "plain", "bibtex_reference_style": "super"},
)
def test_citation_roles_super(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text(encoding="utf-8-sig")
    # just a cursory check that superscript references are present
    assert '<sup><a class="reference internal" href="#' in output


@pytest.mark.sphinx(
    "pseudoxml",
    testroot="debug_bibtex_citation",
    confoverrides={"bibtex_reference_style": "non_existing"},
)
def test_citation_style_invalid(make_app, app_params) -> None:
    args, kwargs = app_params
    with pytest.raises(ImportError, match="plugin .*non_existing not found"):
        make_app(*args, **kwargs)


def my_bracket() -> BracketStyle:
    return BracketStyle(
        left="(",
        right=")",
        sep="; ",
        sep2="; ",
        last_sep="; ",
    )


def my_person() -> PersonStyle:
    return PersonStyle(
        style="last",
        abbreviate=False,
        sep=" & ",
        sep2=None,
        last_sep=None,
        other=" et al",
    )


@dataclass
class CustomReferenceStyle(AuthorYearReferenceStyle):
    bracket_textual: BracketStyle = field(default_factory=my_bracket)
    bracket_parenthetical: BracketStyle = field(default_factory=my_bracket)
    bracket_author: BracketStyle = field(default_factory=my_bracket)
    bracket_label: BracketStyle = field(default_factory=my_bracket)
    bracket_year: BracketStyle = field(default_factory=my_bracket)
    person: PersonStyle = field(default_factory=my_person)
    author_year_sep: str = " "


sphinxcontrib.bibtex.plugin.register_plugin(
    "sphinxcontrib.bibtex.style.referencing", "xxx_custom_xxx", CustomReferenceStyle
)


@pytest.mark.sphinx(
    "text",
    testroot="citation_roles",
    confoverrides={"bibtex_reference_style": "xxx_custom_xxx"},
)
def test_citation_style_custom(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.txt").read_text(encoding="utf-8-sig")
    tests = [
        ("p", " (de Du et al 2003) "),
        ("ps", " (de Du & Em & Fa 2003) "),
        ("t", " de Du et al (2003) "),
        ("ts", " de Du & Em & Fa (2003) "),
        ("ct", " De Du et al (2003) "),
        ("cts", " De Du & Em & Fa (2003) "),
        ("labelpar", " (dDEF03) "),
        ("label", " dDEF03 "),
        ("yearpar", " (2003) "),
        ("year", " 2003 "),
        ("authorpar", " (de Du et al) "),
        ("authorpars", " (de Du & Em & Fa) "),
        ("author", " de Du et al "),
        ("authors", " de Du & Em & Fa "),
        ("cauthor", " De Du et al "),
        ("cauthors", " De Du & Em & Fa "),
        ("empty", " AAA  AAA "),
        ("p", " (al Ap 2001; Be & Ci 2002) "),
        ("ps", " (al Ap 2001; Be & Ci 2002) "),
        ("t", " al Ap (2001); Be & Ci (2002) "),
        ("ts", " al Ap (2001); Be & Ci (2002) "),
        ("ct", " Al Ap (2001); Be & Ci (2002) "),
        ("cts", " Al Ap (2001); Be & Ci (2002) "),
        ("labelpar", " (aA01; BC02) "),
        ("label", " aA01; BC02 "),
        ("yearpar", " (2001; 2002) "),
        ("year", " 2001; 2002 "),
        ("authorpar", " (al Ap; Be & Ci) "),
        ("authorpars", " (al Ap; Be & Ci) "),
        ("author", " al Ap; Be & Ci "),
        ("authors", " al Ap; Be & Ci "),
        ("cauthor", " Al Ap; Be & Ci "),
        ("cauthors", " Al Ap; Be & Ci "),
        ("empty", " BBB  BBB "),
        ("p", " (Ge 2004; Hu 2005; Ix 2006) "),
        ("ps", " (Ge 2004; Hu 2005; Ix 2006) "),
        ("t", " Ge (2004); Hu (2005); Ix (2006) "),
        ("ts", " Ge (2004); Hu (2005); Ix (2006) "),
        ("ct", " Ge (2004); Hu (2005); Ix (2006) "),
        ("cts", " Ge (2004); Hu (2005); Ix (2006) "),
        ("labelpar", " (Ge04; Hu05; Ix06) "),
        ("label", " Ge04; Hu05; Ix06 "),
        ("yearpar", " (2004; 2005; 2006) "),
        ("year", " 2004; 2005; 2006 "),
        ("authorpar", " (Ge; Hu; Ix) "),
        ("authorpars", " (Ge; Hu; Ix) "),
        ("author", " Ge; Hu; Ix "),
        ("authors", " Ge; Hu; Ix "),
        ("cauthor", " Ge; Hu; Ix "),
        ("cauthors", " Ge; Hu; Ix "),
        ("empty", " CCC  CCC "),
    ]
    for role, text in tests:
        escaped_text = re.escape(text)
        pattern = f'":cite:{role}:".*{escaped_text}'
        assert re.search(pattern, output) is not None
    # check :cite:empty: generates citation
    assert "[Ju07] Jo Ju. Testseven. 2007." in output


@pytest.mark.sphinx("text", testroot="citation_style_round_brackets")
def test_citation_style_round_brackets(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.txt").read_text(encoding="utf-8-sig")
    assert "(Evensen, 2003)" in output
    assert "Evensen (2003)" in output


@pytest.mark.sphinx("html", testroot="citation_toctree")
def test_citation_toctree(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text(encoding="utf-8-sig")
    output1 = (app.outdir / "adoc1.html").read_text(encoding="utf-8-sig")
    output2 = (app.outdir / "adoc2.html").read_text(encoding="utf-8-sig")
    assert len(html_citations(label="1").findall(output)) == 1
    assert len(html_citation_refs(label="1").findall(output1)) == 1
    assert len(html_docutils_citation_refs(label=r"Test2").findall(output2)) == 1
    assert len(html_citations(label="Test2").findall(output2)) == 1


@pytest.mark.sphinx("html", testroot="debug_bibtex_citation")
def test_citation_tooltip(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text(encoding="utf-8-sig")
    assert len(html_citations(label="tes").findall(output)) == 1
    assert (
        len(html_citation_refs(label="tes", title=r"The title\.").findall(output)) == 1
    )


@pytest.mark.sphinx(
    "html", testroot="debug_bibtex_citation", confoverrides={"bibtex_tooltips": False}
)
def test_citation_tooltip2(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text(encoding="utf-8-sig")
    assert len(html_citations(label="tes").findall(output)) == 1
    assert len(html_citation_refs(label="tes", title=None).findall(output)) == 1


class CustomTooltipStyle(UnsrtStyle):
    def get_misc_template(self, e):
        return words["whoop whoop"]


pybtex.plugin.register_plugin(
    "pybtex.style.formatting", "xxx_custom_tooltip_xxx", CustomTooltipStyle
)


@pytest.mark.sphinx(
    "html",
    testroot="debug_bibtex_citation",
    confoverrides={"bibtex_tooltips_style": "xxx_custom_tooltip_xxx"},
)
def test_citation_tooltip3(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text(encoding="utf-8-sig")
    assert len(html_citations(label="tes").findall(output)) == 1
    assert (
        len(html_citation_refs(label="tes", title="whoop whoop").findall(output)) == 1
    )


# https://bitbucket.org/pybtex-devs/pybtex/issues/442/author-names-with-special-latex-characters
@pytest.mark.xfail(reason="upstream bug")
@pytest.mark.sphinx("html", testroot="citation_label_special_chars")
def test_citation_label_special_chars(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text(encoding="utf-8-sig")
    assert len(html_citations(label="SBV09").findall(output)) == 1
