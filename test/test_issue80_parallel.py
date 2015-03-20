"""
    test_issue80
    ~~~~~~~~~~~~

    Test parallel build.
"""

import re
from six import StringIO

from util import path, with_app

srcdir = path(__file__).parent.joinpath('issue80').abspath()
warnfile = StringIO()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warning=warnfile, parallel=8)
def test_issue80_parallel(app):
    app.builder.build_all()
    warnings = warnfile.getvalue()
    assert re.search(
        'the sphinxcontrib.bibtex extension is not safe for parallel '
        'reading, doing serial read', warnings)
