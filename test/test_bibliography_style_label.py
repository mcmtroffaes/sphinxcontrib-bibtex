import common
import pytest


@pytest.mark.sphinx('html', testroot='bibliography_style_label')
def test_bibliography_style_label(app, warning):
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text()
    assert len(common.html_citation_refs(label='APAa').findall(output)) == 1
    assert len(common.html_citation_refs(label='APAb').findall(output)) == 1
