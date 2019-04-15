# -*- coding: utf-8 -*-
"""
    test_issue15
    ~~~~~~~~~~~~

    Test order of bibliography entries when using an unsorted style.
"""

import re
from sphinx_testing.util import path, with_app


srcdir = path(__file__).dirname().joinpath('issue15').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warningiserror=True)
def test_duplicate_label(app, status, warning):
    app.builder.build_all()
    output = (path(app.outdir) / "index.html").read_text()
    assert re.search(
        '<dd>.*Test 1.*</dd>.*<dd>.*Test 2.*</dd>',
        output, re.DOTALL)
