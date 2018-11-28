# -*- coding: utf-8 -*-
"""
    test_latex_refs
    ~~~~~~~~~~~~~~~

    Check that LaTeX backend produces correct references.
"""

import re
import sphinx
from sphinx_testing.util import path, with_app

srcdir = path(__file__).dirname().joinpath('latex_refs').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warningiserror=True, buildername='latex')
def test_latex_refs(app, status, warning):
    app.builder.build_all()
    output = (app.outdir / "test.tex").read_text(encoding='utf-8')
    if sphinx.version_info >= (1, 8):
        assert r'\sphinxcite{contents:huygens}' in output
        assert r'\bibitem[Huy57]{contents:huygens}' in output
    else:
        assert re.search(
            r'\\hyperref\[(\\detokenize{)?contents:huygens(})?\]', output)
        assert re.search(
            r'\\label{(\\detokenize{)?contents:huygens(})?}}', output)
