# -*- coding: utf-8 -*-
"""
    test_subfolder
    ~~~~~~~~~~~

    Test bib files in subfolder.
"""

import nose.tools
from sphinx_testing.util import path, with_app


srcdir = path(__file__).dirname().joinpath('subfolder').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warningiserror=True)
def test_sphinx(app, status, warning):
    app.builder.build_all()
