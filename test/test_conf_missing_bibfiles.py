# -*- coding: utf-8 -*-
"""
    test_conf_missing_bibfiles
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Test missing bibfiles configuration variable.
"""

import nose.tools
from sphinx.errors import ExtensionError
from sphinx_testing.util import path, with_app

srcdir = path(__file__).dirname().joinpath('conf_missing_bibfiles').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@nose.tools.raises(ExtensionError)
@with_app(srcdir=srcdir, warningiserror=True)
def test_conf_missing_bibfiles(app, status, warning):
    pass
