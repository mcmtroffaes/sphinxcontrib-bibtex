# -*- coding: utf-8 -*-
"""
    test_list_citation
    ~~~~~~~~~~~~~~~~~~

    Test the ``:list: citation`` option.
"""

import os.path
import re

from util import path, with_app

srcdir = path(__file__).parent.joinpath('list_citation').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warningiserror=True)
def test_list_citation(app):
    app.builder.build_all()
    with open(os.path.join(app.outdir, "contents.html")) as stream:
        assert re.search(
            '<p id="bibtex-bibliography-contents-0">'
            '.*<tr><td class="label">\\[1\\]</td><td>.*Akkerdju.*</td></tr>'
            '.*<tr><td class="label">\\[2\\]</td><td>.*Bro.*</td></tr>'
            '.*<tr><td class="label">\\[3\\]</td><td>.*Chap.*</td></tr>'
            '.*<tr><td class="label">\\[4\\]</td><td>.*Dude.*</td></tr>'
            '.*</p>',
            stream.read(), re.MULTILINE | re.DOTALL)
