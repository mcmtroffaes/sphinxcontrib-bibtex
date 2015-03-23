# -*- coding: utf-8 -*-
"""
    test_issue2
    ~~~~~~~~~~~

    Test mixing of ``:cite:`` and ``[]_``.
"""

import nose.tools

from sphinx_testing.util import path, with_app

srcdir = path(__file__).dirname().joinpath('issue2').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warningiserror=True)
def test_mixing_citation_styles(app, status, warning):
    app.builder.build_all()
    nose.tools.assert_equal(
        app.env.bibtex_cache.get_cited_docnames(u"Test"), {u"adoc1"})
    nose.tools.assert_equal(
        app.env.bibtex_cache.get_label_from_key(u"Test"), u"1")
