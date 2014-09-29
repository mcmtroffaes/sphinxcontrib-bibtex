# -*- coding: utf-8 -*-
"""
    test_invalid_cite_option
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Test behaviour when invalid cite option is given.
"""

import re
from sphinx_testing.util import path, with_app


srcdir = path(__file__).dirname().joinpath('invalid_cite_option').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir)
def test_invalid_cite_option(app, status, warning):
    app.builder.build_all()
    assert re.search(
        'unknown option: "thisisintentionallyinvalid"', warning.getvalue())
