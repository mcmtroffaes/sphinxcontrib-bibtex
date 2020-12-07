"""
    test_issue91
    ~~~~~~~~~~~~

    Test bibtex_default_style config value.
"""

import pytest
import re


@pytest.mark.sphinx('html', testroot='issue91')
def test_issue91(app, warning):
    app.builder.build_all()
    assert not warning.getvalue()
    # default style is plain; check output
    output = (app.outdir / "index.html").read_text()
    # ensure Man09 is cited with plain style and not with alpha style
    assert len(re.findall("\\[1\\]", output)) == 1
    assert len(re.findall("\\[Man09\\]", output)) == 0
