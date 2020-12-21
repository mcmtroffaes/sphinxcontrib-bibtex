# -*- coding: utf-8 -*-
"""
    test_sphinx
    ~~~~~~~~~~~

    General Sphinx test and check output.
"""
from typing import cast

import pytest

from sphinxcontrib.bibtex import BibtexCitationDomain


@pytest.mark.sphinx('html', testroot='sphinx')
def test_sphinx(app, warning):
    app.build()
    warnings = warning.getvalue()
    assert u'could not relabel citation' not in warnings
    assert u'is not referenced' in warnings
    # for coverage
    with pytest.raises(KeyError):
        domain = cast(BibtexCitationDomain, app.env.get_domain('cite'))
        domain.get_label_from_key("nonexistinglabel")
