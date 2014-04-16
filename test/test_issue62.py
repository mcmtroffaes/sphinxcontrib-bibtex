# -*- coding: utf-8 -*-
"""
    test_issue62
    ~~~~~~~~~~~~

    Test local bibliographies.
"""

import nose.tools

from util import path, with_app

srcdir = path(__file__).parent.joinpath('issue62').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warningiserror=True)
def test_local_bibliographies(app):
    app.builder.build_all()
    # TODO test bibliographic entries from the actual generated html files
