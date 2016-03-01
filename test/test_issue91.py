"""
    test_issue91
    ~~~~~~~~~~~~

    Test bibtex_default_style config value.
"""

import os.path
import re

from sphinx_testing.util import path, with_app

srcdir = path(__file__).dirname().joinpath('issue91').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warningiserror=True)
def test_issue91(app, status, warning):
    app.builder.build_all()
    # default style is plain; check output
    with open(os.path.join(app.outdir, "contents.html")) as stream:
        output = stream.read()
        # ensure Man09 is cited with plain style and not with alpha style
        assert len(re.findall('\\[1\\]', output)) == 2
        assert len(re.findall('\\[Man09\\]', output)) == 0
