"""
    test_issue205
    ~~~~~~~~~~~~

    Test cites spanning multiple lines.
"""

import os.path
import re

from sphinx_testing.util import path, with_app

srcdir = path(__file__).dirname().joinpath('issue205').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warningiserror=True)
def test_issue91(app, status, warning):
    app.builder.build_all()
    with open(os.path.join(app.outdir, "index.html")) as stream:
        output = stream.read()
        # ensure Man09 is cited
        assert len(re.findall("\\[Fir\\]", output)) == 1
        assert len(re.findall("\\[Sec\\]", output)) == 1
