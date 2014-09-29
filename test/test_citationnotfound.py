# -*- coding: utf-8 -*-
"""
    test_citationnotfound
    ~~~~~~~~~~~~~~~~~~~~~

    Citation not found check.
"""

import re
from sphinx_testing.util import path, with_app


srcdir = path(__file__).dirname().joinpath('citationnotfound').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir)
def test_citationnotfound(app, status, warning):
    app.builder.build_all()
    assert re.search('citation not found: nosuchkey', warning.getvalue())
