# -*- coding: utf-8 -*-
"""
    test_issue187
    ~~~~~~~~~~~~~

    Test multiple footbibliography directives.
"""

from sphinx_testing.util import path, with_app

srcdir = path(__file__).dirname().joinpath('issue187').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warningiserror=True)
def test_issue187(app, status, warning):
    app.builder.build_all()
    output = (path(app.outdir) / "index.html").read_text(encoding='utf-8')
