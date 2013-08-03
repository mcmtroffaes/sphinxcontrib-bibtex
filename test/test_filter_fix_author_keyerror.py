# -*- coding: utf-8 -*-
"""
    test_filter_fix_author_keyerror
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Test for a bug in the filter option.
"""

from util import path, with_app

srcdir = path(__file__).parent.joinpath('filter_fix_author_keyerror').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warningiserror=True)
def test_filter_fix_author_keyerror(app):
    app.builder.build_all()
