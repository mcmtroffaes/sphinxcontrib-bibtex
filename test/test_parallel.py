"""Test for parallel build."""

from sphinx.util.parallel import parallel_available
import pytest


@pytest.mark.skipif(not parallel_available,
                    reason='sphinx parallel builds not available')
@pytest.mark.sphinx('html', testroot='parallel')
def test_parallel(app, warning):
    app.parallel = 4
    app.build()
    assert not warning.getvalue()
