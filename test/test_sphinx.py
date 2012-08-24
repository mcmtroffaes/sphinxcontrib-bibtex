# -*- coding: utf-8 -*-
"""
    test_sphinx
    ~~~~~~~~~~~

    General Sphinx test and check output.
"""

import nose.tools
import re
from StringIO import StringIO

from util import *

srcdir = path(__file__).parent.joinpath('sphinx').abspath()
warnfile = StringIO()

def teardown_module():
    (srcdir / '_build').rmtree(True)

@with_app(srcdir=srcdir, warning=warnfile)
def test_sphinx(app):
    app.builder.build_all()
    warnings = warnfile.getvalue()
    assert re.search(u'could not relabel citation \\[Test01\\]', warnings)
    assert re.search(u'could not relabel citation \\[Test02\\]', warnings)
    assert re.search(u'could not relabel citation \\[Wa04\\]', warnings)
    assert re.search(u'could not relabel citation reference \\[Test01\\]', warnings)
    assert re.search(u'could not relabel citation reference \\[Test02\\]', warnings)
    assert re.search(u'could not relabel citation reference \\[Wa04\\]', warnings)
