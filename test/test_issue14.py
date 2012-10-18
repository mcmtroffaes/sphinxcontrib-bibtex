# -*- coding: utf-8 -*-
"""
    test_issue14
    ~~~~~~~~~~~~

    Test duplicate label issue.
"""

import nose.tools
from StringIO import StringIO
import os.path
import re

from util import *

srcdir = path(__file__).parent.joinpath('issue14').abspath()
warnfile = StringIO()

def teardown_module():
    (srcdir / '_build').rmtree(True)

@with_app(srcdir=srcdir, warning=warnfile)
def test_duplicate_label(app):
    app.builder.build_all()
    warnings = warnfile.getvalue()
    assert re.search('duplicate label for keys (Test and Test2)|(Test2 and Test)', warnings)
    with open(os.path.join(app.outdir, "doc1.html")) as stream:
        assert re.search('<td class="label">\\[1\\]</td>', stream.read())
    with open(os.path.join(app.outdir, "doc2.html")) as stream:
        assert re.search('<td class="label">\\[1\\]</td>', stream.read())
