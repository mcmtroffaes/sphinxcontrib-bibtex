# -*- coding: utf-8 -*-
"""
    test_filter_option_clash
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Test filter option clash with all, cited, and notcited.
"""

import re
from sphinx_testing.util import path, with_app


srcdir = path(__file__).dirname().joinpath('filter_option_clash').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir)
def test_filter_option_clash(app, status, warning):
    app.builder.build_all()
    warnings = warning.getvalue()
    assert re.search(':filter: overrides :all:', warnings)
    assert re.search(':filter: overrides :cited:', warnings)
    assert re.search(':filter: overrides :notcited:', warnings)
