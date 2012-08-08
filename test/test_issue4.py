# -*- coding: utf-8 -*-
"""
    test_issue4
    ~~~~~~~~~~~

    Test the ``:encoding:`` option.
"""

import nose.tools
from StringIO import StringIO
import os.path
import re

from util import *

srcdir = path(__file__).parent.joinpath('issue4').abspath()

def teardown_module():
    (srcdir / '_build').rmtree(True)

@with_app(srcdir=srcdir, warningiserror=True)
def test_encoding(app):
    app.builder.build_all()
    with open(os.path.join(app.outdir, "index.html")) as stream:
        assert re.search("Tést☺", stream.read())
