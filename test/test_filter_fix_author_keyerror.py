# -*- coding: utf-8 -*-
"""
    test_filter_fix_author_keyerror
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Test for a bug in the filter option.
"""

from sphinx_testing.util import path, with_app


srcdir = path(__file__).dirname().joinpath(
    'filter_fix_author_keyerror').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warningiserror=True)
def test_filter_fix_author_keyerror(app, status, warning):
    app.builder.build_all()
