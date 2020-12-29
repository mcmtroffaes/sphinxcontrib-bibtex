import common
import pytest


@pytest.mark.sphinx('html', testroot='issue91')
def test_issue91(app, warning):
    app.build()
    assert not warning.getvalue()
    # default style is plain; check output
    output = (app.outdir / "index.html").read_text()
    # ensure Man09 is cited with plain style and not with alpha style
    assert len(common.html_citation_refs(label="1").findall(output)) == 1
    assert len(common.html_citation_refs(label="Man09").findall(output)) == 0
