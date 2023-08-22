import pytest


@pytest.mark.sphinx("html", testroot="spurious_div")
def test_spurious_div(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text()
    assert output.count("<div") == output.count("</div>")


@pytest.mark.sphinx("html", testroot="spurious_div_2")
def test_spurious_div_2(app) -> None:
    # note: build will generate warning, is expected, not checking
    app.build()
    output = (app.outdir / "index.html").read_text()
    assert output.count("<div") == output.count("</div>")
