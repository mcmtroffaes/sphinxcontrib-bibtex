import pytest


@pytest.mark.sphinx('html', testroot='citation_not_found')
def test_citation_not_found(app, warning):
    app.build()
    assert 'could not find bibtex key nosuchkey1' in warning.getvalue()
    assert 'could not find bibtex key nosuchkey2' in warning.getvalue()
