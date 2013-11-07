# -*- coding: utf-8 -*-
"""
    test_list_bullet
    ~~~~~~~~~~~~~~~~

    Test the ``:list: bullet`` option.
"""

import os.path
import re

from util import path, with_app

srcdir = path(__file__).parent.joinpath('list_bullet').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warningiserror=True)
def test_list_bullet(app):
    app.builder.build_all()
    with open(os.path.join(app.outdir, "contents.html")) as stream:
        assert re.search(
            '<ul .* id="bibtex-bibliography-contents-0">'
            '.*<li>.*Akkerdju.*</li>'
            '.*<li>.*Bro.*</li>'
            '.*<li>.*Chap.*</li>'
            '.*<li>.*Dude.*</li>'
            '.*</ul>',
            stream.read(), re.MULTILINE | re.DOTALL)
