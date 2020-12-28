"""
    test_list_bullet
    ~~~~~~~~~~~~~~~~

    Test the ``:list: bullet`` option.
"""

import pytest
import re


@pytest.mark.sphinx('html', testroot='list_bullet')
def test_list_bullet(app, warning):
    app.builder.build_all()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text()
    assert re.search(
        '<ul'
        '.*<li.*Akkerdju.*</li>'
        '.*<li.*Bro.*</li>'
        '.*<li.*Chap.*</li>'
        '.*<li.*Dude.*</li>'
        '.*</ul>',
        output, re.DOTALL)
