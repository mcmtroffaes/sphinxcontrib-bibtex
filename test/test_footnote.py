# -*- coding: utf-8 -*-
"""
    test_footnote
    ~~~~~~~~~~~~~

    Test for footbib.
"""

from sphinx_testing.util import path, with_app

srcdir = path(__file__).dirname().joinpath('footnote').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warningiserror=True)
def test_footnote(app, status, warning):
    app.builder.build_all()
