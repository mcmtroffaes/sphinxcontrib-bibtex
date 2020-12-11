# -*- coding: utf-8 -*-
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
        '<ul .* id="bibtex-bibliography-index-[0-9]+">'
        '.*<li>.*Akkerdju.*</li>'
        '.*<li>.*Bro.*</li>'
        '.*<li>.*Chap.*</li>'
        '.*<li>.*Dude.*</li>'
        '.*</ul>',
        output, re.MULTILINE | re.DOTALL)
