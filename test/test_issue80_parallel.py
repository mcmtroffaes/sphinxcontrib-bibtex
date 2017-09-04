"""
    test_issue80
    ~~~~~~~~~~~~

    Test parallel build.
"""

from sphinx_testing.util import path, with_app

srcdir = path(__file__).dirname().joinpath('issue80').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, parallel=8)
def test_issue80_parallel(app, status, warning):
    app.builder.build_all()
