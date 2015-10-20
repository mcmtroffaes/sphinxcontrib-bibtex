"""
    test_issue87
    ~~~~~~~~~~~~

    Test bibliography tags.
"""

import os.path
import re

from sphinx_testing.util import path, with_app

srcdir = path(__file__).dirname().joinpath('issue87').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warningiserror=True)
def test_issue87(app, status, warning):
    app.builder.build_all()
    with open(os.path.join(app.outdir, "contents.html")) as stream:
        output = stream.read()
        # TODO test some things
