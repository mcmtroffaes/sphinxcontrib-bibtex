# -*- coding: utf-8 -*-
"""
    test_issue14
    ~~~~~~~~~~~~

    Test duplicate label issue.
"""

import re
from sphinx_testing.util import path, with_app


srcdir = path(__file__).dirname().joinpath('issue14').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir)
def test_duplicate_label(app, status, warning):
    app.builder.build_all()
    assert re.search(
        'duplicate label for keys (Test and Test2)|(Test2 and Test)',
        warning.getvalue())
    output = (app.outdir / "doc1.html").read_text()
    assert re.search('<td class="label">\\[1\\]</td>', output)
    output = (app.outdir / "doc2.html").read_text()
    assert re.search('<td class="label">\\[1\\]</td>', output)
