"""
    test_issue87
    ~~~~~~~~~~~~

    Test bibliography tags.
"""

import re

from sphinx_testing.util import path, with_app

srcdir = path(__file__).dirname().joinpath('issue87').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warningiserror=True)
def test_issue87(app, status, warning):
    app.builder.build_all()
    output = (path(app.outdir) / "doc0.html").read_text(encoding='utf-8')
    assert re.search(
        'class="bibtex reference internal" href="#tag0-2009-mandel"', output)
    assert re.search(
        'class="bibtex reference internal" href="#tag0-2003-evensen"', output)
    assert re.search('AMan09', output)
    assert re.search('AEve03', output)
    output = (path(app.outdir) / "doc1.html").read_text(encoding='utf-8')
    assert re.search(
        'class="bibtex reference internal" href="#tag1-2009-mandel"', output)
    assert not re.search(
        'class="bibtex reference internal" href="#tag1-2003-evensen"', output)
    assert re.search('BMan09', output)
    assert not re.search('BEve03', output)
