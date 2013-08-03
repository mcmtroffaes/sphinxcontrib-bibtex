# -*- coding: utf-8 -*-
"""
    test_issue17
    ~~~~~~~~~~~~

    Test that sphinx [source] links do not generate a warning.
"""

from util import path, with_app

srcdir = path(__file__).parent.joinpath('issue17').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warningiserror=True)
def test_sphinx_source_no_warning(app):
    app.builder.build_all()
