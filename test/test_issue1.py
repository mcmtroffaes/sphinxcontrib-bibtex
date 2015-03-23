# -*- coding: utf-8 -*-
"""
    test_issue1
    ~~~~~~~~~~~

    Test Tinkerer and check output.
"""

import nose.tools

from sphinx_testing.util import path, with_app

srcdir = path(__file__).dirname().joinpath('issue1').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warningiserror=True)
def test_tinker(app, status, warning):
    app.builder.build_all()
    nose.tools.assert_equal(
        app.env.bibtex_cache.get_cited_docnames(u"2011:BabikerIPv6"),
        {u"2012/07/24/hello_world_"})
    nose.tools.assert_equal(
        app.env.bibtex_cache.get_label_from_key(u"2011:BabikerIPv6"), u"BNC11")
