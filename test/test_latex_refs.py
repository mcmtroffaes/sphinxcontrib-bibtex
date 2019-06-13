# -*- coding: utf-8 -*-
"""
    test_latex_refs
    ~~~~~~~~~~~~~~~

    Check that LaTeX backend produces correct references.
"""

from sphinx_testing.util import path, with_app

srcdir = path(__file__).dirname().joinpath('latex_refs').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warningiserror=True, buildername='latex')
def test_latex_refs(app, status, warning):
    app.builder.build_all()
    output = (path(app.outdir) / "test.tex").read_text(encoding='utf-8')
    assert r'\sphinxcite{index:huygens}' in output
    assert r'\bibitem[Huy57]{index:huygens}' in output
