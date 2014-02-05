# -*- coding: utf-8 -*-
"""
    test_custom_style
    ~~~~~~~~~~~~~~~~~

    Test a custom style.
"""

import os.path
import re

from util import path, with_app
from nose.tools import nottest
from nose import SkipTest

srcdir = path(__file__).parent.joinpath('custom_style').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


def test_custom_style_skip():
    raise SkipTest("this test is disabled until pybtex 0.17 is out")


@nottest
@with_app(srcdir=srcdir, warningiserror=True)
def test_custom_style(app):
    app.builder.build_all()
    with open(os.path.join(app.outdir, "contents.html")) as stream:
        output = stream.read()
        # the custom style suppresses web links
        assert not re.search('http://arxiv.org', output)
        assert not re.search('http://dx.doi.org', output)
