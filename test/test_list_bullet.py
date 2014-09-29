# -*- coding: utf-8 -*-
"""
    test_list_bullet
    ~~~~~~~~~~~~~~~~

    Test the ``:list: bullet`` option.
"""

import re

from sphinx_testing.util import path, with_app

srcdir = path(__file__).dirname().joinpath('list_bullet').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warningiserror=True)
def test_list_bullet(app, status, warning):
    app.builder.build_all()
    output = (app.outdir / "contents.html").read_text()
    assert re.search(
        '<ul .* id="bibtex-bibliography-contents-0">'
        '.*<li>.*Akkerdju.*</li>'
        '.*<li>.*Bro.*</li>'
        '.*<li>.*Chap.*</li>'
        '.*<li>.*Dude.*</li>'
        '.*</ul>',
        output, re.MULTILINE | re.DOTALL)
