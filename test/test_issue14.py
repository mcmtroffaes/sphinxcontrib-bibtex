# -*- coding: utf-8 -*-
"""
    test_issue14
    ~~~~~~~~~~~~

    Test duplicate label issue.
"""

import pytest
import re


def htmlbiblabel(label):
    return (
        r'<dt class="label".*><span class="brackets">\[{0}\]</span>'
        .format(label))


@pytest.mark.sphinx('html', testroot='issue14')
def test_duplicate_label(app, warning):
    app.builder.build_all()
    assert re.search(
        r"duplicate label \[1] for keys ({'Test', 'Test2'})|({'Test2', 'Test'})",
        warning.getvalue())
    output = (app.outdir / "doc1.html").read_text()
    assert re.search(htmlbiblabel("1"), output)
    output = (app.outdir / "doc2.html").read_text()
    assert re.search(htmlbiblabel("1"), output)
