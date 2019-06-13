# -*- coding: utf-8 -*-
"""
    test_issue61
    ~~~~~~~~~~~~

    Test multiple keys in a single cite.
"""

import re
from sphinx_testing.util import path, with_app

srcdir = path(__file__).dirname().joinpath('issue61').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warningiserror=True)
def test_multiple_keys(app, status, warning):
    app.builder.build_all()
    output = (path(app.outdir) / "index.html").read_text(encoding='utf-8')
    assert re.search(
        'class="bibtex reference internal" href="#testone"', output)
    assert re.search(
        'class="bibtex reference internal" href="#testtwo"', output)
