"""
    test_natbib
    ~~~~~~~~~~~

    Test the natbib extension, which serves as an example for comparison.
"""

import pytest


@pytest.mark.sphinx("html", testroot="natbib")
def test_natbib(app, warning) -> None:
    app.build()
    assert not warning.getvalue()


@pytest.mark.sphinx("latex", testroot="natbib")
def test_natbib_latex(app, warning) -> None:
    app.build()
    assert not warning.getvalue()


@pytest.mark.sphinx("html", testroot="natbib_keynotfound")
def test_natbib_keynotfound(app, warning) -> None:
    app.build()
    warning.seek(0)
    warnings = warning.readlines()
    assert len(warnings) == 1
    assert "WARNING: cite-key `XXX` not found in bibtex file" in warnings[0]


@pytest.mark.sphinx("html", testroot="natbib_norefs")
def test_natbib_norefs(app, warning) -> None:
    app.build()
    warning.seek(0)
    warnings = warning.readlines()
    assert len(warnings) == 1
    assert "WARNING: no `refs` directive found" in warnings[0]


def test_natbib_citation_transform_str_repr() -> None:
    from test.natbib import DEFAULT_CONF, CitationTransform

    from pybtex.database import Entry

    ref = Entry(type_="misc")
    ref.key = "somekey"
    node = CitationTransform(
        pre="",
        post="",
        typ="cite:p",
        global_keys={},
        config=DEFAULT_CONF.copy(),
        refs=[ref],
    )
    assert str(node) == "somekey"
    assert repr(node) == "<somekey>"


@pytest.mark.sphinx("text", testroot="natbib_conf")
def test_natbib_conf(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.txt").read_text()
    assert "{One, 2001/ Two, 2002}" in output
