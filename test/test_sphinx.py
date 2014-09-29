# -*- coding: utf-8 -*-
"""
    test_sphinx
    ~~~~~~~~~~~

    General Sphinx test and check output.
"""

import re
from sphinx_testing.util import path, with_app


srcdir = path(__file__).dirname().joinpath('sphinx').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir)
def test_sphinx(app, status, warning):
    app.builder.build_all()
    warnings = warning.getvalue()
    assert re.search(u'could not relabel citation \\[Test01\\]', warnings)
    assert re.search(u'could not relabel citation \\[Test02\\]', warnings)
    assert re.search(u'could not relabel citation \\[Wa04\\]', warnings)
    assert re.search(
        u'could not relabel citation reference \\[Test01\\]',
        warnings)
    assert re.search(
        u'could not relabel citation reference \\[Test02\\]',
        warnings)
    assert re.search(
        u'could not relabel citation reference \\[Wa04\\]',
        warnings)
