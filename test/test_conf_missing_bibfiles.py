# -*- coding: utf-8 -*-
"""
    test_conf_missing_bibfiles
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Test missing bibfiles configuration variable.
"""

import pytest
from sphinx.errors import ExtensionError


@pytest.mark.sphinx('html', testroot='conf_missing_bibfiles')
def test_conf_missing_bibfiles(make_app, app_params):
    args, kwargs = app_params
    with pytest.raises(ExtensionError):
        make_app(*args, **kwargs)
