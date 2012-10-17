# -*- coding: utf-8 -*-
"""
    test_issue14_2
    ~~~~~~~~~~~~~~

    Test labelprefix option.
"""

import nose.tools
from StringIO import StringIO
import os.path
import re

from util import *

srcdir = path(__file__).parent.joinpath('issue14_2').abspath()

def teardown_module():
    (srcdir / '_build').rmtree(True)

@with_app(srcdir=srcdir, warningiserror=True)
def test_label_prefix(app):
    app.builder.build_all()
    with open(os.path.join(app.outdir, "doc1.html")) as stream:
        assert re.search('<td class="label">\\[A1\\]</td>', stream.read())
    with open(os.path.join(app.outdir, "doc2.html")) as stream:
        assert re.search('<td class="label">\\[B1\\]</td>', stream.read())
