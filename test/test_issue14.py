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
        '<dt class="bibtex label".*><span class="brackets">{0}</span></dt>'
        .format(label))


@pytest.mark.sphinx('html', testroot='issue14')
def test_duplicate_label(app, warning):
    app.builder.build_all()
    assert re.search(
        'duplicate label for keys (Test and Test2)|(Test2 and Test)',
        warning.getvalue())
    output = (app.outdir / "doc1.html").read_text(encoding='utf-8')
    assert re.search(htmlbiblabel("1"), output)
    output = (app.outdir / "doc2.html").read_text(encoding='utf-8')
    assert re.search(htmlbiblabel("1"), output)
