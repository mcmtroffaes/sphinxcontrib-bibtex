# -*- coding: utf-8 -*-
"""
    test_issue_173
    ~~~~~~~~~~~~~~

    Check referencing works with near identical entries.
"""

from sphinx_testing.util import path, with_app

srcdir = path(__file__).dirname().joinpath('issue_173').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warningiserror=True)
def test_issue_173(app, status, warning):
    app.builder.build_all()
    output = (path(app.outdir) / "index.html").read_text(encoding='utf-8')
    assert "[xyz19a]" in output
    assert "[xyz19b]" in output
