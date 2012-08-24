# -*- coding: utf-8 -*-
"""
    test_issue1
    ~~~~~~~~~~~

    Test Tinkerer and check output.
"""

import nose.tools
from StringIO import StringIO

from util import *

srcdir = path(__file__).parent.joinpath('issue1').abspath()

def teardown_module():
    (srcdir / '_build').rmtree(True)

@with_app(srcdir=srcdir, warningiserror=True)
def test_tinker(app):
    app.builder.build_all()
    nose.tools.assert_true(app.env.bibtex_cache.is_cited(u"2011:BabikerIPv6"))
    nose.tools.assert_equal(
        app.env.bibtex_cache.get_label_from_key(u"2011:BabikerIPv6"), u"1")
