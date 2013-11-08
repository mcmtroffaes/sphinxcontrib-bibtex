# -*- coding: utf-8 -*-
"""
    test_latex_refs
    ~~~~~~~~~~~~~~~

    Check that LaTeX backend produces correct references.
"""

import os
import re
from util import path, with_app

srcdir = path(__file__).parent.joinpath('latex_refs').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warningiserror=True, buildername='latex')
def test_latex_refs(app):
    app.builder.build_all()
    with open(os.path.join(app.outdir, "test.tex")) as stream:
        code = stream.read()
        assert re.search('\\hyperref\[contents:huygens\]', code)
        assert re.search('\\label{contents:huygens}', code)
