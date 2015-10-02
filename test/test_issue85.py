"""
    test_issue77
    ~~~~~~~~~~~~

    Test for reference with no author and no key.
"""

from sphinx_testing.util import path, with_app

srcdir = path(__file__).dirname().joinpath('issue85').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warningiserror=True)
def test_issue77(app, status, warning):
    app.builder.build_all()
