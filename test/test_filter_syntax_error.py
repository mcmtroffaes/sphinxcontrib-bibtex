# -*- coding: utf-8 -*-
"""
    test_filter_syntax_error
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Test response on syntax errors in filter.
"""

import nose.tools
from six import StringIO
import re

from util import path, with_app

srcdir = path(__file__).parent.joinpath('filter_syntax_error').abspath()
warnfile = StringIO()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warning=warnfile)
def test_filter_syntax_error(app):
    app.builder.build_all()
    warnings = warnfile.getvalue()
    nose.tools.assert_equal(
        len(re.findall('syntax error in :filter: expression', warnings)), 9)
