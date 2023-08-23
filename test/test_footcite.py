import re
from dataclasses import dataclass, field

import pytest

import sphinxcontrib.bibtex.plugin
from sphinxcontrib.bibtex.style.referencing import BracketStyle, PersonStyle
from sphinxcontrib.bibtex.style.referencing.foot import FootReferenceStyle


@pytest.mark.sphinx("text", testroot="footcite_roles")
def test_footcite_roles(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.txt").read_text(encoding="utf-8-sig")
    tests = [
        ("p", " [1] "),
        ("ps", " [1] "),
        ("t", " de Du *et al.*[1] "),
        ("ts", " de Du, Em, and Fa[1] "),
        ("ct", " De Du *et al.*[1] "),
        ("cts", " De Du, Em, and Fa[1] "),
        ("p", " [2][3] "),
        ("ps", " [2][3] "),
        ("t", " al Ap[2], Be and Ci[3] "),
        ("ts", " al Ap[2], Be and Ci[3] "),
        ("ct", " Al Ap[2], Be and Ci[3] "),
        ("cts", " Al Ap[2], Be and Ci[3] "),
        ("p", " [4][5][6] "),
        ("ps", " [4][5][6] "),
        ("t", " Ge[4], Hu[5], Ix[6] "),
        ("ts", " Ge[4], Hu[5], Ix[6] "),
        ("ct", " Ge[4], Hu[5], Ix[6] "),
        ("cts", " Ge[4], Hu[5], Ix[6] "),
    ]
    for role, text in tests:
        escaped_text = re.escape(text)
        pattern = f'":footcite:{role}:".*{escaped_text}'
        assert re.search(pattern, output) is not None


def my_bracket() -> BracketStyle:
    return BracketStyle(
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
class CustomReferenceStyle(FootReferenceStyle):
    bracket_textual: BracketStyle = field(default_factory=my_bracket)
    person: PersonStyle = field(default_factory=my_person)


sphinxcontrib.bibtex.plugin.register_plugin(
    "sphinxcontrib.bibtex.style.referencing",
    "xxx_foot_custom_xxx",
    CustomReferenceStyle,
)


@pytest.mark.sphinx(
    "text",
    testroot="footcite_roles",
    confoverrides={"bibtex_foot_reference_style": "xxx_foot_custom_xxx"},
)
def test_footcite_style_custom(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.txt").read_text(encoding="utf-8-sig")
    tests = [
        ("p", " [1] "),
        ("ps", " [1] "),
        ("t", " de Du et al[1] "),
        ("ts", " de Du & Em & Fa[1] "),
        ("ct", " De Du et al[1] "),
        ("cts", " De Du & Em & Fa[1] "),
        ("p", " [2][3] "),
        ("ps", " [2][3] "),
        ("t", " al Ap[2]; Be & Ci[3] "),
        ("ts", " al Ap[2]; Be & Ci[3] "),
        ("ct", " Al Ap[2]; Be & Ci[3] "),
        ("cts", " Al Ap[2]; Be & Ci[3] "),
        ("p", " [4][5][6] "),
        ("ps", " [4][5][6] "),
        ("t", " Ge[4]; Hu[5]; Ix[6] "),
        ("ts", " Ge[4]; Hu[5]; Ix[6] "),
        ("ct", " Ge[4]; Hu[5]; Ix[6] "),
        ("cts", " Ge[4]; Hu[5]; Ix[6] "),
    ]
    for role, text in tests:
        escaped_text = re.escape(text)
        pattern = f'":footcite:{role}:".*{escaped_text}'
        assert re.search(pattern, output) is not None


@pytest.mark.sphinx("text", testroot="footcite_roles_pre_post")
def test_footcite_pre_post(app, warning) -> None:
    app.build()
    bad_keys = ["{see}testthree", "testthree{p. 1}", "{see}testthree{p. 1}"]
    for bad_key in bad_keys:
        assert f'could not find bibtex key "{bad_key}"' in warning.getvalue()
