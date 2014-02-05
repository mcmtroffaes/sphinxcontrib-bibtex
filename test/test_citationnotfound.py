# -*- coding: utf-8 -*-
"""
    test_citationnotfound
    ~~~~~~~~~~~~~~~~~~~~~

    Citation not found check.
"""

import re
from six import StringIO

from util import path, with_app

srcdir = path(__file__).parent.joinpath('citationnotfound').abspath()
warnfile = StringIO()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warning=warnfile)
def test_citationnotfound(app):
    app.builder.build_all()
    warnings = warnfile.getvalue()
    assert re.search('citation not found: nosuchkey', warnings)
