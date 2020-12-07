# -*- coding: utf-8 -*-
"""
    test_filter_option_clash
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Test filter option clash with all, cited, and notcited.
"""

import pytest
import re


@pytest.mark.sphinx('html', testroot='filter_option_clash')
def test_filter_option_clash(app, warning):
    app.builder.build_all()
    warnings = warning.getvalue()
    assert re.search(':filter: overrides :all:', warnings)
    assert re.search(':filter: overrides :cited:', warnings)
    assert re.search(':filter: overrides :notcited:', warnings)
