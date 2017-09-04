"""
    test_issue77
    ~~~~~~~~~~~~

    Test label style.
"""

import io
import os.path
import re

from sphinx_testing.util import path, with_app

srcdir = path(__file__).dirname().joinpath('issue77').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warningiserror=True)
def test_issue77(app, status, warning):
    app.builder.build_all()
    with io.open(os.path.join(app.outdir, "contents.html"), encoding='utf-8') as stream:
        output = stream.read()
        assert len(re.findall('\\[APAa\\]', output)) == 2
        assert len(re.findall('\\[APAb\\]', output)) == 2
