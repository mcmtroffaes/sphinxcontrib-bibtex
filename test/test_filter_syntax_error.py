# -*- coding: utf-8 -*-
"""
    test_filter_syntax_error
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Test response on syntax errors in filter.
"""

import nose.tools
import re
from sphinx_testing.util import path, with_app


srcdir = path(__file__).dirname().joinpath('filter_syntax_error').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir)
def test_filter_syntax_error(app, status, warning):
    app.builder.build_all()
    nose.tools.assert_equal(
        len(re.findall(
            'syntax error in :filter: expression', warning.getvalue())), 9)
