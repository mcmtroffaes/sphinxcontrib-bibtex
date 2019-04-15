"""
    test_issue77
    ~~~~~~~~~~~~

    Test label style.
"""

import re

from sphinx_testing.util import path, with_app

srcdir = path(__file__).dirname().joinpath('issue77').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warningiserror=True)
def test_issue77(app, status, warning):
    app.builder.build_all()
    output = (path(app.outdir) / "index.html").read_text(encoding='utf-8')
    assert len(re.findall('\\[APAa\\]', output)) == 1
    assert len(re.findall('\\[APAb\\]', output)) == 1
