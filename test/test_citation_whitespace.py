import common
import pytest


# test cites spanning multiple lines (issue 205)
@pytest.mark.sphinx('html', testroot='citation_whitespace')
def test_citation_whitespace(app, warning):
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text()
    # ensure Man09 is cited
    assert len(common.html_citation_refs(label='Fir').findall(output)) == 1
    assert len(common.html_citation_refs(label='Sec').findall(output)) == 1
