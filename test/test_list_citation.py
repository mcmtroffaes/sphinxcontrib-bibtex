"""
    test_list_citation
    ~~~~~~~~~~~~~~~~~~

    Test the ``:list: citation`` option.
"""

import common
import pytest


@pytest.mark.sphinx('html', testroot='list_citation')
def test_list_citation(app, warning):
    app.builder.build_all()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text()
    assert common.html_citations(label='1', text='.*Akkerdju.*').search(output)
    assert common.html_citations(label='2', text='.*Bro.*').search(output)
    assert common.html_citations(label='3', text='.*Chap.*').search(output)
    assert common.html_citations(label='4', text='.*Dude.*').search(output)
