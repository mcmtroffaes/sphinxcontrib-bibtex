# -*- coding: utf-8 -*-
"""
    test_issue15
    ~~~~~~~~~~~~

    Test order of bibliography entries when using an unsorted style.
"""

from six import StringIO
import os.path
import re

from util import path, with_app

srcdir = path(__file__).parent.joinpath('issue15').abspath()
warnfile = StringIO()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warningiserror=True)
def test_duplicate_label(app):
    app.builder.build_all()
    with open(os.path.join(app.outdir, "contents.html")) as stream:
        assert re.search(
            '<tr>.*Test 1.*</tr>.*<tr>.*Test 2.*</tr>',
            stream.read(), re.DOTALL)
