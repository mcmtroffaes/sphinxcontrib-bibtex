# -*- coding: utf-8 -*-
"""
    test_filter
    ~~~~~~~~~~~

    Test filter option.
"""

import re
import pytest


@pytest.mark.sphinx('html', testroot='filter')
def test_filter(app, warning):
    app.builder.build_all()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text(encoding='utf-8')
    assert re.search('Tralalala', output)
    assert not re.search('ideetje', output)
    assert not re.search('Jakkamakka', output)
    output = (app.outdir / "or.html").read_text(encoding='utf-8')
    assert not re.search('Tralalala', output)
    assert re.search('ideetje', output)
    assert re.search('Jakkamakka', output)
    output = (app.outdir / "noteq.html").read_text(encoding='utf-8')
    assert re.search('Tralalala', output)
    assert re.search('ideetje', output)
    assert not re.search('Jakkamakka', output)
    output = (app.outdir / "lt.html").read_text(encoding='utf-8')
    assert re.search('Tralalala', output)
    assert not re.search('ideetje', output)
    assert not re.search('Jakkamakka', output)
    output = (app.outdir / "lte.html").read_text(encoding='utf-8')
    assert re.search('Tralalala', output)
    assert not re.search('ideetje', output)
    assert re.search('Jakkamakka', output)
    output = (app.outdir / "gt.html").read_text(encoding='utf-8')
    assert not re.search('Tralalala', output)
    assert re.search('ideetje', output)
    assert not re.search('Jakkamakka', output)
    output = (app.outdir / "gte.html").read_text(encoding='utf-8')
    assert not re.search('Tralalala', output)
    assert re.search('ideetje', output)
    assert re.search('Jakkamakka', output)
    output = (app.outdir / "key.html").read_text(encoding='utf-8')
    assert not re.search('Tralalala', output)
    assert re.search('ideetje', output)
    assert not re.search('Jakkamakka', output)
    output = (app.outdir / "false.html").read_text(encoding='utf-8')
    assert not re.search('Tralalala', output)
    assert not re.search('ideetje', output)
    assert not re.search('Jakkamakka', output)
    output = (app.outdir / "true.html").read_text(encoding='utf-8')
    assert re.search('Tralalala', output)
    assert re.search('ideetje', output)
    assert re.search('Jakkamakka', output)
    output = (app.outdir / "title.html").read_text(encoding='utf-8')
    assert not re.search('Tralalala', output)
    assert not re.search('ideetje', output)
    assert re.search('Jakkamakka', output)
