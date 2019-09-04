# -*- coding: utf-8 -*-
"""
    test_custom_style
    ~~~~~~~~~~~~~~~~~

    Test a custom label style.
"""

from sphinx_testing.util import path, with_app

srcdir = path(__file__).dirname().joinpath('custom_labels').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warningiserror=True)
def test_custom_labels(app, status, warning):
    app.builder.build_all()
    output = (path(app.outdir) / "index.html").read_text(encoding='utf-8')
    # the custom style uses keys as labels
    print(output)
    assert "[myfancybibtexkey]" in output
    assert "[myotherfancybibtexkey]" in output
    assert ">myfancybibtexkey</a>" in output
    assert ">myotherfancybibtexkey</a>" in output
