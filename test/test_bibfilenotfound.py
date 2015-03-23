# -*- coding: utf-8 -*-
"""
    test_bibfilenotfound
    ~~~~~~~~~~~~~~~~~~~~

    Bib file not found check.
"""

import re
from sphinx_testing.util import path, with_app


srcdir = path(__file__).dirname().joinpath('bibfilenotfound').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir)
def test_bibfilenotfound(app, status, warning):
    app.builder.build_all()
    assert re.search(
        'could not open bibtex file .*unknown[.]bib', warning.getvalue())
