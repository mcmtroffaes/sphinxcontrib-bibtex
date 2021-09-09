from test.common import html_citations, html_citation_refs
import dataclasses
import pytest
import re
import sphinxcontrib.bibtex.plugin

from sphinxcontrib.bibtex.domain import BibtexDomain
from typing import cast

from sphinxcontrib.bibtex.style.referencing import \
    BracketStyle, PersonStyle
from sphinxcontrib.bibtex.style.referencing.author_year import \
    AuthorYearReferenceStyle


@pytest.mark.sphinx('html', testroot='citation_not_found')
def test_citation_not_found(app, warning) -> None:
    app.build()
    assert 'could not find bibtex key "nosuchkey1"' in warning.getvalue()
    assert 'could not find bibtex key "nosuchkey2"' in warning.getvalue()


# test mixing of ``:cite:`` and ``[]_`` (issue 2)
@pytest.mark.sphinx('html', testroot='citation_mixed')
def test_citation_mixed(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    domain = cast(BibtexDomain, app.env.get_domain('cite'))
    assert len(domain.citation_refs) == 1
    citation_ref = domain.citation_refs.pop()
    assert citation_ref.keys == ['Test']
    assert citation_ref.docname == 'adoc1'
    assert len(domain.citations) == 1
    citation = domain.citations.pop()
    assert citation.formatted_entry.label == '1'


@pytest.mark.sphinx('html', testroot='citation_multiple_keys')
def test_citation_multiple_keys(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text()
    cits = {match.group('label')
            for match in html_citations().finditer(output)}
    citrefs = {match.group('label')
               for match in html_citation_refs().finditer(output)}
    assert {"App", "Bra"} == cits == citrefs


@pytest.mark.sphinx('html', testroot='citation_any_role')
def test_citation_any_role(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text()
    cits = {match.group('label')
            for match in html_citations().finditer(output)}
    citrefs = {match.group('label')
               for match in html_citation_refs().finditer(output)}
    assert {"App", "Bra"} == cits == citrefs


def find_label(output: str, label: str):
    assert html_citation_refs(label=label).search(output) is not None


# see issue 85
@pytest.mark.sphinx('html', testroot='citation_no_author_no_key')
def test_citation_no_author_no_key(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text()
    find_label(output, "<em>Software projects built on Mesos</em>, 2015")
    find_label(output, "2015")
    find_label(output, "Mandel, 2009")
    find_label(output, "2009")
    find_label(output, "<em>This citation only has a title</em>, n.d.")
    find_label(output, "n.d.")
    find_label(output, "Whatever, 2021")
    find_label(output, "2021")


# test cites spanning multiple lines (issue 205)
@pytest.mark.sphinx('html', testroot='citation_whitespace')
def test_citation_whitespace(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text()
    # ensure Man09 is cited
    assert len(html_citation_refs(label='Fir').findall(output)) == 1
    assert len(html_citation_refs(label='Sec').findall(output)) == 1


# test document not in toctree (issue 228)
@pytest.mark.sphinx('pseudoxml', testroot='citation_from_orphan')
def test_citation_from_orphan(app, warning) -> None:
    app.build()
    assert not warning.getvalue()


@pytest.mark.sphinx('text', testroot='citation_roles')
def test_citation_roles_label(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.txt").read_text()
    tests = [
        ("p",           " [dDEF03] "),
        ("ps",          " [dDEF03] "),
        ("t",           " de Du *et al.* [dDEF03] "),
        ("ts",          " de Du, Em, and Fa [dDEF03] "),
        ("ct",          " De Du *et al.* [dDEF03] "),
        ("cts",         " De Du, Em, and Fa [dDEF03] "),
        ("labelpar",    " [dDEF03] "),
        ("label",       " dDEF03 "),
        ("yearpar",     " [2003] "),
        ("year",        " 2003 "),
        ("authorpar",   " [de Du *et al.*] "),
        ("authorpars",  " [de Du, Em, and Fa] "),
        ("author",      " de Du *et al.* "),
        ("authors",     " de Du, Em, and Fa "),
        ("cauthor",     " De Du *et al.* "),
        ("cauthors",    " De Du, Em, and Fa "),
        ("empty",       " AAA  AAA "),
        ("p",           " [aA01, BC02] "),
        ("ps",          " [aA01, BC02] "),
        ("t",           " al Ap [aA01], Be and Ci [BC02] "),
        ("ts",          " al Ap [aA01], Be and Ci [BC02] "),
        ("ct",          " Al Ap [aA01], Be and Ci [BC02] "),
        ("cts",         " Al Ap [aA01], Be and Ci [BC02] "),
        ("labelpar",    " [aA01, BC02] "),
        ("label",       " aA01, BC02 "),
        ("yearpar",     " [2001, 2002] "),
        ("year",        " 2001, 2002 "),
        ("authorpar",   " [al Ap, Be and Ci] "),
        ("authorpars",  " [al Ap, Be and Ci] "),
        ("author",      " al Ap, Be and Ci "),
        ("authors",     " al Ap, Be and Ci "),
        ("cauthor",     " Al Ap, Be and Ci "),
        ("cauthors",    " Al Ap, Be and Ci "),
        ("empty",       " BBB  BBB "),
        ("p",           " [Ge04, Hu05, Ix06] "),
        ("ps",          " [Ge04, Hu05, Ix06] "),
        ("t",           " Ge [Ge04], Hu [Hu05], Ix [Ix06] "),
        ("ts",          " Ge [Ge04], Hu [Hu05], Ix [Ix06] "),
        ("ct",          " Ge [Ge04], Hu [Hu05], Ix [Ix06] "),
        ("cts",         " Ge [Ge04], Hu [Hu05], Ix [Ix06] "),
        ("labelpar",    " [Ge04, Hu05, Ix06] "),
        ("label",       " Ge04, Hu05, Ix06 "),
        ("yearpar",     " [2004, 2005, 2006] "),
        ("year",        " 2004, 2005, 2006 "),
        ("authorpar",   " [Ge, Hu, Ix] "),
        ("authorpars",  " [Ge, Hu, Ix] "),
        ("author",      " Ge, Hu, Ix "),
        ("authors",     " Ge, Hu, Ix "),
        ("cauthor",     " Ge, Hu, Ix "),
        ("cauthors",    " Ge, Hu, Ix "),
        ("empty",       " CCC  CCC "),
    ]
    for role, text in tests:
        escaped_text = re.escape(text)
        pattern = f'":cite:{role}:".*{escaped_text}'
        assert re.search(pattern, output) is not None
    # check :cite:empty: generates citation
    assert "[Ju07] Jo Ju. Testseven. 2007." in output


@pytest.mark.sphinx(
    'text', testroot='citation_roles',
    confoverrides={'bibtex_reference_style': 'author_year'})
def test_citation_roles_authoryear(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.txt").read_text()
    tests = [
        ("p",           " [de Du *et al.*, 2003] "),
        ("ps",          " [de Du, Em, and Fa, 2003] "),
        ("t",           " de Du *et al.* [2003] "),
        ("ts",          " de Du, Em, and Fa [2003] "),
        ("ct",          " De Du *et al.* [2003] "),
        ("cts",         " De Du, Em, and Fa [2003] "),
        ("labelpar",    " [dDEF03] "),
        ("label",       " dDEF03 "),
        ("yearpar",     " [2003] "),
        ("year",        " 2003 "),
        ("authorpar",   " [de Du *et al.*] "),
        ("authorpars",  " [de Du, Em, and Fa] "),
        ("author",      " de Du *et al.* "),
        ("authors",     " de Du, Em, and Fa "),
        ("cauthor",     " De Du *et al.* "),
        ("cauthors",    " De Du, Em, and Fa "),
        ("empty",       " AAA  AAA "),
        ("p",           " [al Ap, 2001, Be and Ci, 2002] "),
        ("ps",          " [al Ap, 2001, Be and Ci, 2002] "),
        ("t",           " al Ap [2001], Be and Ci [2002] "),
        ("ts",          " al Ap [2001], Be and Ci [2002] "),
        ("ct",          " Al Ap [2001], Be and Ci [2002] "),
        ("cts",         " Al Ap [2001], Be and Ci [2002] "),
        ("labelpar",    " [aA01, BC02] "),
        ("label",       " aA01, BC02 "),
        ("yearpar",     " [2001, 2002] "),
        ("year",        " 2001, 2002 "),
        ("authorpar",   " [al Ap, Be and Ci] "),
        ("authorpars",  " [al Ap, Be and Ci] "),
        ("author",      " al Ap, Be and Ci "),
        ("authors",     " al Ap, Be and Ci "),
        ("cauthor",     " Al Ap, Be and Ci "),
        ("cauthors",    " Al Ap, Be and Ci "),
        ("empty",       " BBB  BBB "),
        ("p",           " [Ge, 2004, Hu, 2005, Ix, 2006] "),
        ("ps",          " [Ge, 2004, Hu, 2005, Ix, 2006] "),
        ("t",           " Ge [2004], Hu [2005], Ix [2006] "),
        ("ts",          " Ge [2004], Hu [2005], Ix [2006] "),
        ("ct",          " Ge [2004], Hu [2005], Ix [2006] "),
        ("cts",         " Ge [2004], Hu [2005], Ix [2006] "),
        ("labelpar",    " [Ge04, Hu05, Ix06] "),
        ("label",       " Ge04, Hu05, Ix06 "),
        ("yearpar",     " [2004, 2005, 2006] "),
        ("year",        " 2004, 2005, 2006 "),
        ("authorpar",   " [Ge, Hu, Ix] "),
        ("authorpars",  " [Ge, Hu, Ix] "),
        ("author",      " Ge, Hu, Ix "),
        ("authors",     " Ge, Hu, Ix "),
        ("cauthor",     " Ge, Hu, Ix "),
        ("cauthors",    " Ge, Hu, Ix "),
        ("empty", " CCC  CCC "),
    ]
    for role, text in tests:
        escaped_text = re.escape(text)
        pattern = f'":cite:{role}:".*{escaped_text}'
        assert re.search(pattern, output) is not None
    # check :cite:empty: generates citation
    assert "[Ju07] Jo Ju. Testseven. 2007." in output


@pytest.mark.sphinx(
    'html', testroot='citation_roles',
    confoverrides={'bibtex_default_style': 'plain',
                   'bibtex_reference_style': 'super'})
def test_citation_roles_super(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text()
    # just a cursory check that superscript references are present
    assert '<sup><a class="reference internal" href="#' in output


@pytest.mark.sphinx('pseudoxml', testroot='debug_bibtex_citation',
                    confoverrides={'bibtex_reference_style': 'non_existing'})
def test_citation_style_invalid(make_app, app_params) -> None:
    args, kwargs = app_params
    with pytest.raises(ImportError, match='plugin .*non_existing not found'):
        make_app(*args, **kwargs)


my_bracket = BracketStyle(
    left='(',
    right=')',
    sep='; ',
    sep2='; ',
    last_sep='; ',
)


my_person = PersonStyle(
    style='last',
    abbreviate=False,
    sep=' & ',
    sep2=None,
    last_sep=None,
    other=' et al',
)


@dataclasses.dataclass
class CustomReferenceStyle(AuthorYearReferenceStyle):
    bracket_textual: BracketStyle = my_bracket
    bracket_parenthetical: BracketStyle = my_bracket
    bracket_author: BracketStyle = my_bracket
    bracket_label: BracketStyle = my_bracket
    bracket_year: BracketStyle = my_bracket
    person: PersonStyle = my_person
    author_year_sep: str = ' '


sphinxcontrib.bibtex.plugin.register_plugin(
    'sphinxcontrib.bibtex.style.referencing',
    'xxx_custom_xxx', CustomReferenceStyle)


@pytest.mark.sphinx('text', testroot='citation_roles',
                    confoverrides={
                        'bibtex_reference_style': 'xxx_custom_xxx'})
def test_citation_style_custom(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.txt").read_text()
    tests = [
        ("p",           " (de Du et al 2003) "),
        ("ps",          " (de Du & Em & Fa 2003) "),
        ("t",           " de Du et al (2003) "),
        ("ts",          " de Du & Em & Fa (2003) "),
        ("ct",          " De Du et al (2003) "),
        ("cts",         " De Du & Em & Fa (2003) "),
        ("labelpar",    " (dDEF03) "),
        ("label",       " dDEF03 "),
        ("yearpar",     " (2003) "),
        ("year",        " 2003 "),
        ("authorpar",   " (de Du et al) "),
        ("authorpars",  " (de Du & Em & Fa) "),
        ("author",      " de Du et al "),
        ("authors",     " de Du & Em & Fa "),
        ("cauthor",     " De Du et al "),
        ("cauthors",    " De Du & Em & Fa "),
        ("empty",       " AAA  AAA "),
        ("p",           " (al Ap 2001; Be & Ci 2002) "),
        ("ps",          " (al Ap 2001; Be & Ci 2002) "),
        ("t",           " al Ap (2001); Be & Ci (2002) "),
        ("ts",          " al Ap (2001); Be & Ci (2002) "),
        ("ct",          " Al Ap (2001); Be & Ci (2002) "),
        ("cts",         " Al Ap (2001); Be & Ci (2002) "),
        ("labelpar",    " (aA01; BC02) "),
        ("label",       " aA01; BC02 "),
        ("yearpar",     " (2001; 2002) "),
        ("year",        " 2001; 2002 "),
        ("authorpar",   " (al Ap; Be & Ci) "),
        ("authorpars",  " (al Ap; Be & Ci) "),
        ("author",      " al Ap; Be & Ci "),
        ("authors",     " al Ap; Be & Ci "),
        ("cauthor",     " Al Ap; Be & Ci "),
        ("cauthors",    " Al Ap; Be & Ci "),
        ("empty",       " BBB  BBB "),
        ("p",           " (Ge 2004; Hu 2005; Ix 2006) "),
        ("ps",          " (Ge 2004; Hu 2005; Ix 2006) "),
        ("t",           " Ge (2004); Hu (2005); Ix (2006) "),
        ("ts",          " Ge (2004); Hu (2005); Ix (2006) "),
        ("ct",          " Ge (2004); Hu (2005); Ix (2006) "),
        ("cts",         " Ge (2004); Hu (2005); Ix (2006) "),
        ("labelpar",    " (Ge04; Hu05; Ix06) "),
        ("label",       " Ge04; Hu05; Ix06 "),
        ("yearpar",     " (2004; 2005; 2006) "),
        ("year",        " 2004; 2005; 2006 "),
        ("authorpar",   " (Ge; Hu; Ix) "),
        ("authorpars",  " (Ge; Hu; Ix) "),
        ("author",      " Ge; Hu; Ix "),
        ("authors",     " Ge; Hu; Ix "),
        ("cauthor",     " Ge; Hu; Ix "),
        ("cauthors",    " Ge; Hu; Ix "),
        ("empty",       " CCC  CCC "),
    ]
    for role, text in tests:
        escaped_text = re.escape(text)
        pattern = f'":cite:{role}:".*{escaped_text}'
        assert re.search(pattern, output) is not None
    # check :cite:empty: generates citation
    assert "[Ju07] Jo Ju. Testseven. 2007." in output


@pytest.mark.sphinx('text', testroot='citation_style_round_brackets')
def test_citation_style_round_brackets(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.txt").read_text()
    assert "(Evensen, 2003)" in output
    assert "Evensen (2003)" in output
