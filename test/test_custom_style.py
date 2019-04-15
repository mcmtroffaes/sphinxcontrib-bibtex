# -*- coding: utf-8 -*-
"""
    test_custom_style
    ~~~~~~~~~~~~~~~~~

    Test a custom style.
"""

import re

from sphinx_testing.util import path, with_app

srcdir = path(__file__).dirname().joinpath('custom_style').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warningiserror=True)
def test_custom_style(app, status, warning):
    app.builder.build_all()
    output = (path(app.outdir) / "index.html").read_text(encoding='utf-8')
    # the custom style suppresses web links
    assert not re.search('http://arxiv.org', output)
    assert not re.search('http://dx.doi.org', output)
