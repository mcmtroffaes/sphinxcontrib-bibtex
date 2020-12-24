"""Some tests purely used for stepping into the debugger
to help understand what docutils/sphinx are doing.
"""

import pytest


@pytest.mark.sphinx('html', testroot='debug_citation')
def test_debug_citation(app, warning):
    """A simple test with a single standard docutils citation."""
    app.build()
    assert not warning.getvalue()
