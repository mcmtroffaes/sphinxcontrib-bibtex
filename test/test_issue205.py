"""
    test_issue205
    ~~~~~~~~~~~~~

    Test cites spanning multiple lines.
"""

import re
import pytest


@pytest.mark.sphinx('html', testroot='issue205')
def test_issue205(app, warning):
    app.builder.build_all()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text()
    # ensure Man09 is cited
    assert len(re.findall("\\[Fir\\]", output)) == 1
    assert len(re.findall("\\[Sec\\]", output)) == 1
