import pytest


@pytest.mark.sphinx('html', testroot='header')
def test_header(app, warning):
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text(encoding='utf-8')
    assert 'Regular Citations' in output
    assert 'Footnote Citations' in output
