# -*- coding: utf-8 -*-
"""
    test_issue17
    ~~~~~~~~~~~~

    Test that sphinx [source] links do not generate a warning.
"""

from sphinx_testing.util import path, with_app

srcdir = path(__file__).dirname().joinpath('issue17').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warningiserror=True)
def test_sphinx_source_no_warning(app, status, warning):
    app.builder.build_all()
