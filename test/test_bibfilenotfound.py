# -*- coding: utf-8 -*-
"""
    test_bibfilenotfound
    ~~~~~~~~~~~~~~~~~~~~

    Bib file not found check.
"""

import pytest
import re


@pytest.mark.sphinx('html', testroot='bibfilenotfound')
def test_bibfilenotfound(app, warning):
    app.builder.build_all()
    assert re.search(
        'could not open bibtex file .*unknown[.]bib', warning.getvalue())
