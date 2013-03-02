# -*- coding: utf-8 -*-
"""
    test_issue17
    ~~~~~~~~~~~~

    Test that sphinx [source] links do not generate a warning.
"""

import nose.tools
from StringIO import StringIO
import os.path
import re

from util import *

srcdir = path(__file__).parent.joinpath('issue17').abspath()
warnfile = StringIO()

def teardown_module():
    (srcdir / '_build').rmtree(True)

@with_app(srcdir=srcdir, warningiserror=True)
def test_sphinx_source_no_warning(app):
    app.builder.build_all()
