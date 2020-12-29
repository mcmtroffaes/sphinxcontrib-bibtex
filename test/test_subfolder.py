"""
    test_subfolder
    ~~~~~~~~~~~

    Test bib files in subfolder.
"""

import pytest


@pytest.mark.sphinx('html', testroot='subfolder')
def test_sphinx(app, warning):
    app.build()
    assert not warning.getvalue()
