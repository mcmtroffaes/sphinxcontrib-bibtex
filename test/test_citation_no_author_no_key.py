import pytest


# see issue 85
@pytest.mark.sphinx('html', testroot='citation_no_author_no_key')
def test_citation_no_author_no_key(app, warning):
    app.build()
    assert not warning.getvalue()
