"""
    test_issue77
    ~~~~~~~~~~~~

    Test label style.
"""

import pytest
import re


@pytest.mark.sphinx('html', testroot='issue77')
def test_issue77(app, warning):
    app.builder.build_all()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text(encoding='utf-8')
    assert len(re.findall('\\[APAa\\]', output)) == 1
    assert len(re.findall('\\[APAb\\]', output)) == 1
