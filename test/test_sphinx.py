# -*- coding: utf-8 -*-
"""
    test_sphinx
    ~~~~~~~~~~~

    General Sphinx test and check output.
"""

import pytest


@pytest.mark.sphinx('html', testroot='sphinx')
def test_sphinx(app, warning):
    app.build()
    warnings = warning.getvalue()
    assert u'could not relabel citation' not in warnings
    assert u'is not referenced' in warnings
    # for coverage
    with pytest.raises(KeyError):
        app.env.bibtex_cache.get_label_from_key("nonexistinglabel")
