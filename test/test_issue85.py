"""
    test_issue77
    ~~~~~~~~~~~~

    Test for reference with no author and no key.
"""

import pytest


@pytest.mark.sphinx('html', testroot='issue85')
def test_issue77(app, warning):
    app.builder.build_all()
    assert not warning.getvalue()
