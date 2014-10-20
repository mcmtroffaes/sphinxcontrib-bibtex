"""
    test_issue77
    ~~~~~~~~~~~~

    Test label style.
"""

import os.path
import re

from util import path, with_app

srcdir = path(__file__).parent.joinpath('issue77').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warningiserror=True)
def test_issue77(app):
    app.builder.build_all()
    with open(os.path.join(app.outdir, "contents.html")) as stream:
        output = stream.read()
        assert len(re.findall('\\[APAa\\]', output)) == 2
        assert len(re.findall('\\[APAb\\]', output)) == 2
