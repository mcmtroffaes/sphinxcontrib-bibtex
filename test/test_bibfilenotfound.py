# -*- coding: utf-8 -*-
"""
    test_bibfilenotfound
    ~~~~~~~~~~~~~~~~~~~~

    Bib file not found check.
"""

import re
from six import StringIO

from util import path, with_app

srcdir = path(__file__).parent.joinpath('bibfilenotfound').abspath()
warnfile = StringIO()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warning=warnfile)
def test_bibfilenotfound(app):
    app.builder.build_all()
    warnings = warnfile.getvalue()
    assert re.search('could not open bibtex file .*unknown[.]bib', warnings)
