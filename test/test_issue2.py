# -*- coding: utf-8 -*-
"""
    test_issue2
    ~~~~~~~~~~~

    Test mixing of ``:cite:`` and ``[]_``.
"""

import nose.tools
from StringIO import StringIO

from util import *

srcdir = path(__file__).parent.joinpath('issue2').abspath()

def teardown_module():
    (srcdir / '_build').rmtree(True)

@with_app(srcdir=srcdir, warningiserror=True)
def test_mixing_citation_styles(app):
    app.builder.build_all()
    nose.tools.assert_true(app.env.bibtex_cache.is_cited(u"Test"))
    nose.tools.assert_equal(
        app.env.bibtex_cache.get_label_from_key(u"Test"), u"1")
