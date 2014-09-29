# -*- coding: utf-8 -*-
"""
    test_citationnotfound
    ~~~~~~~~~~~~~~~~~~~~~

    Citation not found check.
"""

import re
from six import StringIO

from sphinx_testing.util import path, with_app

srcdir = path(__file__).dirname().joinpath('citationnotfound').abspath()
warnfile = StringIO()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warning=warnfile)
def test_citationnotfound(app, status, warning):
    app.builder.build_all()
    warnings = warnfile.getvalue()
    assert re.search('citation not found: nosuchkey', warnings)
