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
    output = (app.outdir / "contents.html").read_text()
    assert re.search('Tralalala', output)
    assert not re.search('ideetje', output)
    assert not re.search('Jakkamakka', output)
    output = (app.outdir / "or.html").read_text()
    assert not re.search('Tralalala', output)
    assert re.search('ideetje', output)
    assert re.search('Jakkamakka', output)
    output = (app.outdir / "noteq.html").read_text()
    assert re.search('Tralalala', output)
    assert re.search('ideetje', output)
    assert not re.search('Jakkamakka', output)
    output = (app.outdir / "lt.html").read_text()
    assert re.search('Tralalala', output)
    assert not re.search('ideetje', output)
    assert not re.search('Jakkamakka', output)
    output = (app.outdir / "lte.html").read_text()
    assert re.search('Tralalala', output)
    assert not re.search('ideetje', output)
    assert re.search('Jakkamakka', output)
    output = (app.outdir / "gt.html").read_text()
    assert not re.search('Tralalala', output)
    assert re.search('ideetje', output)
    assert not re.search('Jakkamakka', output)
    output = (app.outdir / "gte.html").read_text()
    assert not re.search('Tralalala', output)
    assert re.search('ideetje', output)
    assert re.search('Jakkamakka', output)
    output = (app.outdir / "key.html").read_text()
    assert not re.search('Tralalala', output)
    assert re.search('ideetje', output)
    assert not re.search('Jakkamakka', output)
    output = (app.outdir / "false.html").read_text()
    assert not re.search('Tralalala', output)
    assert not re.search('ideetje', output)
    assert not re.search('Jakkamakka', output)
    output = (app.outdir / "title.html").read_text()
    assert not re.search('Tralalala', output)
    assert not re.search('ideetje', output)
    assert re.search('Jakkamakka', output)
