import pytest


@pytest.mark.sphinx('html', testroot='footcite_empty')
def test_footcite_empty(app, warning):
    app.build()
    assert not warning.getvalue()
