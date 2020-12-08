# -*- coding: utf-8 -*-
"""
    test_issue14_2
    ~~~~~~~~~~~~~~

    Test labelprefix option.
"""

import pytest
import re


@pytest.mark.sphinx('html', testroot='issue14_2')
def test_label_prefix(app, warning):
    app.builder.build_all()
    assert not warning.getvalue()
    output = (app.outdir / "doc1.html").read_text(encoding='utf-8')
    assert re.search('\\[A1\\]', output)
    output = (app.outdir / "doc2.html").read_text(encoding='utf-8')
    assert re.search('\\[B1\\]', output)
