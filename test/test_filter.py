# -*- coding: utf-8 -*-
"""
    test_filter
    ~~~~~~~~~~~

    Test filter option.
"""

import os.path
import re

from util import path, with_app

srcdir = path(__file__).parent.joinpath('filter').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warningiserror=True)
def test_filter(app):
    app.builder.build_all()
    with open(os.path.join(app.outdir, "contents.html")) as stream:
        output = stream.read()
        assert re.search('Tralalala', output)
        assert not re.search('ideetje', output)
        assert not re.search('Jakkamakka', output)
    with open(os.path.join(app.outdir, "or.html")) as stream:
        output = stream.read()
        assert not re.search('Tralalala', output)
        assert re.search('ideetje', output)
        assert re.search('Jakkamakka', output)
    with open(os.path.join(app.outdir, "noteq.html")) as stream:
        output = stream.read()
        assert re.search('Tralalala', output)
        assert re.search('ideetje', output)
        assert not re.search('Jakkamakka', output)
    with open(os.path.join(app.outdir, "lt.html")) as stream:
        output = stream.read()
        assert re.search('Tralalala', output)
        assert not re.search('ideetje', output)
        assert not re.search('Jakkamakka', output)
    with open(os.path.join(app.outdir, "lte.html")) as stream:
        output = stream.read()
        assert re.search('Tralalala', output)
        assert not re.search('ideetje', output)
        assert re.search('Jakkamakka', output)
    with open(os.path.join(app.outdir, "gt.html")) as stream:
        output = stream.read()
        assert not re.search('Tralalala', output)
        assert re.search('ideetje', output)
        assert not re.search('Jakkamakka', output)
    with open(os.path.join(app.outdir, "gte.html")) as stream:
        output = stream.read()
        assert not re.search('Tralalala', output)
        assert re.search('ideetje', output)
        assert re.search('Jakkamakka', output)
    with open(os.path.join(app.outdir, "key.html")) as stream:
        output = stream.read()
        assert not re.search('Tralalala', output)
        assert re.search('ideetje', output)
        assert not re.search('Jakkamakka', output)
    with open(os.path.join(app.outdir, "false.html")) as stream:
        output = stream.read()
        assert not re.search('Tralalala', output)
        assert not re.search('ideetje', output)
        assert not re.search('Jakkamakka', output)
    with open(os.path.join(app.outdir, "title.html")) as stream:
        output = stream.read()
        assert not re.search('Tralalala', output)
        assert not re.search('ideetje', output)
        assert re.search('Jakkamakka', output)
