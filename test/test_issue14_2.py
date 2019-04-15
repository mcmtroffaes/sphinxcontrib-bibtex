# -*- coding: utf-8 -*-
"""
    test_issue14_2
    ~~~~~~~~~~~~~~

    Test labelprefix option.
"""

import re

from sphinx_testing.util import path, with_app

srcdir = path(__file__).dirname().joinpath('issue14_2').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warningiserror=True)
def test_label_prefix(app, status, warning):
    app.builder.build_all()
    output = (path(app.outdir) / "doc1.html").read_text(encoding='utf-8')
    assert re.search('\\[A1\\]', output)
    output = (path(app.outdir) / "doc2.html").read_text(encoding='utf-8')
    assert re.search('\\[B1\\]', output)
