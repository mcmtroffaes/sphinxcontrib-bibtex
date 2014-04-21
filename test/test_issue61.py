# -*- coding: utf-8 -*-
"""
    test_issue61
    ~~~~~~~~~~~~

    Test multiple keys in a single cite.
"""

import os
import re
from util import path, with_app

srcdir = path(__file__).parent.joinpath('issue61').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warningiserror=True)
def test_multiple_keys(app):
    app.builder.build_all()
    with open(os.path.join(app.outdir, "contents.html")) as stream:
        code = stream.read()
        assert re.search('class="reference internal" href="#testone"', code)
        assert re.search('class="reference internal" href="#testtwo"', code)
