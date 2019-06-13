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


def htmlbiblabel(label):
    return (
        '<dt class="bibtex label".*><span class="brackets">{0}</span></dt>'
        .format(label))


@with_app(srcdir=srcdir)
def test_duplicate_label(app, status, warning):
    app.builder.build_all()
    assert re.search(
        'duplicate label for keys (Test and Test2)|(Test2 and Test)',
        warning.getvalue())
    output = (path(app.outdir) / "doc1.html").read_text(encoding='utf-8')
    assert re.search(htmlbiblabel("1"), output)
    output = (path(app.outdir) / "doc2.html").read_text(encoding='utf-8')
    assert re.search(htmlbiblabel("1"), output)
