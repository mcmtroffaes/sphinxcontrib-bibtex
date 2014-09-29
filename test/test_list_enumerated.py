# -*- coding: utf-8 -*-
"""
    test_list_enumerated
    ~~~~~~~~~~~~~~~~~~~~

    Test the ``:list: enumerated`` option.
"""

import re
from sphinx_testing.util import path, with_app


srcdir = path(__file__).dirname().joinpath('list_enumerated').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warningiserror=True)
def test_list_enumerated(app, status, warning):
    app.builder.build_all()
    output = (app.outdir / "contents.html").read_text()
    assert re.search(
        '<ol .*id="bibtex-bibliography-contents-0".* start="1".*>'
        '.*<li>.*Akkerdju.*</li>'
        '.*<li>.*Bro.*</li>'
        '.*<li>.*Chap.*</li>'
        '.*<li>.*Dude.*</li>'
        '.*</ol>'
        '.*<ol .*id="bibtex-bibliography-contents-1".* start="5".*>'
        '.*<li>.*Eminence.*</li>'
        '.*<li>.*Frater.*</li>'
        '.*<li>.*Giggles.*</li>'
        '.*<li>.*Handy.*</li>'
        '.*</ol>'
        '.*<ol .*id="bibtex-bibliography-contents-2".* start="23".*>'
        '.*<li>.*Iedereen.*</li>'
        '.*<li>.*Joke.*</li>'
        '.*<li>.*Klopgeest.*</li>'
        '.*<li>.*Laterfanter.*</li>'
        '.*</ol>',
        output, re.MULTILINE | re.DOTALL)
