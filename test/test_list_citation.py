# -*- coding: utf-8 -*-
"""
    test_list_citation
    ~~~~~~~~~~~~~~~~~~

    Test the ``:list: citation`` option.
"""

import pytest
import re


def htmlbibitem(label, text):
    return (
        '.*<dt class="bibtex label".*><span class="brackets">'
        '<a.*>{0}</a></span></dt>\\s*<dd>.*{1}.*</dd>'.format(label, text))


@pytest.mark.sphinx('html', testroot='list_citation')
def test_list_citation(app, warning):
    app.builder.build_all()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text()
    assert re.search(
        '<p id="bibtex-bibliography-index-[0-9]+">'
        + htmlbibitem("1", "Akkerdju")
        + htmlbibitem("2", "Bro")
        + htmlbibitem("3", "Chap")
        + htmlbibitem("4", "Dude")
        + '.*</p>',
        output, re.MULTILINE | re.DOTALL)
