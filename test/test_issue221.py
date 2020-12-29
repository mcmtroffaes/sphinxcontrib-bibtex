"""
    test_issue221
    ~~~~~~~~~~~~~

    Test missing bibliography_key issue.
"""

import pytest


@pytest.mark.sphinx('latex', testroot='issue221')
def test_issue221(app, warning):
    app.build()
    assert not warning.getvalue()
