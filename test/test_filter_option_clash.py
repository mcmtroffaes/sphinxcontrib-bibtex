# -*- coding: utf-8 -*-
"""
    test_filter_option_clash
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Test filter option clash with all, cited, and notcited.
"""

from six import StringIO
import re

from util import path, with_app

srcdir = path(__file__).parent.joinpath('filter_option_clash').abspath()
warnfile = StringIO()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warning=warnfile)
def test_filter_option_clash(app):
    app.builder.build_all()
    warnings = warnfile.getvalue()
    assert re.search(':filter: overrides :all:', warnings)
    assert re.search(':filter: overrides :cited:', warnings)
    assert re.search(':filter: overrides :notcited:', warnings)
