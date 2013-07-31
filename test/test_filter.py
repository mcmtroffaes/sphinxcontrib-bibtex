# -*- coding: utf-8 -*-
"""
    test_filter
    ~~~~~~~~~~~

    Test filter option.
"""

import nose.tools
import os.path
import re

from util import *

srcdir = path(__file__).parent.joinpath('filter').abspath()

def teardown_module():
    (srcdir / '_build').rmtree(True)

@with_app(srcdir=srcdir, warningiserror=True)
def test_filter(app):
    app.builder.build_all()
    with open(os.path.join(app.outdir, "index.html")) as stream:
        output = stream.read()
        assert re.search('Tralalala', output)
        # TODO uncomment when implemented
        #assert not re.search('ideetje', output)
        #assert not re.search('Jakkamakka', output)
