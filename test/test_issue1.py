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
    nose.tools.assert_equal(
        app.env.bibtex_cache.cited,
        {u'2012/07/24/hello_world_': set([u"2011:BabikerIPv6"])})
    nose.tools.assert_equal(
        app.env.bibtex_cache.bibliographies['bibtex-bibliography-0'].labels,
        {u"2011:BabikerIPv6": "1"})
