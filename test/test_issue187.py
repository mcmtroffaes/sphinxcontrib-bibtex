# -*- coding: utf-8 -*-
"""
    test_issue187
    ~~~~~~~~~~~~~

    Test multiple footbibliography directives.
"""

import re
from sphinx_testing.util import path, with_app

srcdir = path(__file__).dirname().joinpath('issue187').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warningiserror=True)
def test_issue187(app, status, warning):
    app.builder.build_all()
    output = (path(app.outdir) / "index.html").read_text(encoding='utf-8')
    assert len(re.findall(
        'id="bibtex-footbibliography-index-0"', output)) == 1
    assert len(re.findall(
        'id="bibtex-footbibliography-index-1"', output)) == 1
    assert len(re.findall(
        'id="bibtex-footbibliography-index-2"', output)) == 1
    assert len(re.findall('id="mandel"', output)) == 1
    assert len(re.findall('id="evensen"', output)) == 1
    assert len(re.findall('id="lorenc"', output)) == 1
    assert len(re.findall(
        'class="footnote-reference brackets" href="#mandel"', output)) == 2
    assert len(re.findall(
        'class="footnote-reference brackets" href="#evensen"', output)) == 1
    assert len(re.findall(
        'class="footnote-reference brackets" href="#lorenc"', output)) == 1
