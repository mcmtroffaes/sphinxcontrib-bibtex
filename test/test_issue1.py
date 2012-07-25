# -*- coding: utf-8 -*-
"""
    test_issue1
    ~~~~~~~~~~~

    Test Tinkerer and check output.
"""

from StringIO import StringIO

from util import *

srcdir = path(__file__).parent.joinpath('issue1').abspath()

def teardown_module():
    (srcdir / '_build').rmtree(True)

@with_app(srcdir=srcdir, warningiserror=True)
def test_tinker(app):
    app.builder.build_all()
