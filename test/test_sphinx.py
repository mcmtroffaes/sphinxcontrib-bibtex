"""
    test_sphinx
    ~~~~~~~~~~~

    General Sphinx test and check output.
"""

import pytest


@pytest.mark.sphinx('html', testroot='sphinx')
def test_sphinx(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
