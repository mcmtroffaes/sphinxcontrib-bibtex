# -*- coding: utf-8 -*-
"""
    test_filter
    ~~~~~~~~~~~

    Test filter option.
"""

import re
from sphinx_testing.util import path, with_app


srcdir = path(__file__).dirname().joinpath('filter').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warningiserror=True)
def test_filter(app, status, warning):
    app.builder.build_all()
    output = (path(app.outdir) / "index.html").read_text(encoding='utf-8')
    assert re.search('Tralalala', output)
    assert not re.search('ideetje', output)
    assert not re.search('Jakkamakka', output)
    output = (path(app.outdir) / "or.html").read_text(encoding='utf-8')
    assert not re.search('Tralalala', output)
    assert re.search('ideetje', output)
    assert re.search('Jakkamakka', output)
    output = (path(app.outdir) / "noteq.html").read_text(encoding='utf-8')
    assert re.search('Tralalala', output)
    assert re.search('ideetje', output)
    assert not re.search('Jakkamakka', output)
    output = (path(app.outdir) / "lt.html").read_text(encoding='utf-8')
    assert re.search('Tralalala', output)
    assert not re.search('ideetje', output)
    assert not re.search('Jakkamakka', output)
    output = (path(app.outdir) / "lte.html").read_text(encoding='utf-8')
    assert re.search('Tralalala', output)
    assert not re.search('ideetje', output)
    assert re.search('Jakkamakka', output)
    output = (path(app.outdir) / "gt.html").read_text(encoding='utf-8')
    assert not re.search('Tralalala', output)
    assert re.search('ideetje', output)
    assert not re.search('Jakkamakka', output)
    output = (path(app.outdir) / "gte.html").read_text(encoding='utf-8')
    assert not re.search('Tralalala', output)
    assert re.search('ideetje', output)
    assert re.search('Jakkamakka', output)
    output = (path(app.outdir) / "key.html").read_text(encoding='utf-8')
    assert not re.search('Tralalala', output)
    assert re.search('ideetje', output)
    assert not re.search('Jakkamakka', output)
    output = (path(app.outdir) / "false.html").read_text(encoding='utf-8')
    assert not re.search('Tralalala', output)
    assert not re.search('ideetje', output)
    assert not re.search('Jakkamakka', output)
    output = (path(app.outdir) / "true.html").read_text(encoding='utf-8')
    assert re.search('Tralalala', output)
    assert re.search('ideetje', output)
    assert re.search('Jakkamakka', output)
    output = (path(app.outdir) / "title.html").read_text(encoding='utf-8')
    assert not re.search('Tralalala', output)
    assert not re.search('ideetje', output)
    assert re.search('Jakkamakka', output)
