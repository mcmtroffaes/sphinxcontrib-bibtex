import pytest


@pytest.mark.rinohtype
@pytest.mark.sphinx('rinoh', testroot='citation_rinoh')
def test_citation_rinoh(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    # TODO inspect generated pdf


@pytest.mark.rinohtype
@pytest.mark.sphinx('rinoh', testroot='citation_rinoh_multidoc')
def test_citation_rinoh_multidoc(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    # TODO inspect generated pdf
