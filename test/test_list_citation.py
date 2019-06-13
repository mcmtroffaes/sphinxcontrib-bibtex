# -*- coding: utf-8 -*-
"""
    test_list_citation
    ~~~~~~~~~~~~~~~~~~

    Test the ``:list: citation`` option.
"""

import re

from sphinx_testing.util import path, with_app

srcdir = path(__file__).dirname().joinpath('list_citation').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


def htmlbibitem(label, text):
    return (
        '.*<dt class="bibtex label".*><span class="brackets">'
        '<a.*>{0}</a></span></dt>\\s*<dd>.*{1}.*</dd>'.format(label, text))


@with_app(srcdir=srcdir, warningiserror=True)
def test_list_citation(app, status, warning):
    app.builder.build_all()
    output = (path(app.outdir) / "index.html").read_text()
    assert re.search(
        '<p id="bibtex-bibliography-index-0">'
        + htmlbibitem("1", "Akkerdju")
        + htmlbibitem("2", "Bro")
        + htmlbibitem("3", "Chap")
        + htmlbibitem("4", "Dude")
        + '.*</p>',
        output, re.MULTILINE | re.DOTALL)
