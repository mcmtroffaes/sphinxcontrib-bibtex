import pytest


@pytest.mark.sphinx('pseudoxml', testroot='myst_parser')
def test_myst_parser(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
