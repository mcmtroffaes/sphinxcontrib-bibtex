# -*- coding: utf-8 -*-
"""
    test_invalid_cite_option
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Test behaviour when invalid cite option is given.
"""

import re
from six import StringIO

from util import path, with_app

srcdir = path(__file__).parent.joinpath('invalid_cite_option').abspath()
warnfile = StringIO()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warning=warnfile)
def test_invalid_cite_option(app):
    app.builder.build_all()
    warnings = warnfile.getvalue()
    assert re.search('unknown option: "thisisintentionallyinvalid"', warnings)
