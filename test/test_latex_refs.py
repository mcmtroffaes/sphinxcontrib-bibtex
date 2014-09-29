# -*- coding: utf-8 -*-
"""
    test_latex_refs
    ~~~~~~~~~~~~~~~

    Check that LaTeX backend produces correct references.
"""

import re
from sphinx_testing.util import path, with_app

srcdir = path(__file__).dirname().joinpath('latex_refs').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warningiserror=True, buildername='latex')
def test_latex_refs(app, status, warning):
    app.builder.build_all()
    output = (app.outdir / "test.tex").read_text()
    assert re.search('\\hyperref\[contents:huygens\]', output)
    assert re.search('\\label{contents:huygens}', output)
