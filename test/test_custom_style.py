# -*- coding: utf-8 -*-
"""
    test_custom_style
    ~~~~~~~~~~~~~~~~~

    Test a custom style.
"""

import os.path
import re

from util import path, with_app

srcdir = path(__file__).parent.joinpath('custom_style').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warningiserror=True)
def test_custom_style(app):
    app.builder.build_all()
    with open(os.path.join(app.outdir, "index.html")) as stream:
        output = stream.read()
        # the custom style suppresses web links
        assert not re.search('http://arxiv.org', output)
        assert not re.search('http://dx.doi.org', output)
