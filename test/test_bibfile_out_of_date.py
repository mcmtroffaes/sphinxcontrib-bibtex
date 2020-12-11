# -*- coding: utf-8 -*-
"""
    test_bibfile_out_of_date
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Test that updates to the bibfile generate the correct result when
    Sphinx is run again.
"""

import pytest
import re
import shutil
import time


def htmlbibitem(label, text):
    return (
        '.*<dt class="bibtex label".*><span class="brackets">'
        '<a.*>{0}</a></span></dt>\\s*<dd>.*{1}.*</dd>'.format(label, text))


@pytest.mark.sphinx('html', testroot='bibfile_out_of_date')
def test_bibfile_out_of_date(make_app, app_params, warning):
    args, kwargs = app_params
    app = make_app(*args, **kwargs)
    app.build()
    output = (app.outdir / "index.html").read_text()
    assert re.search(
        '<p id="bibtex-bibliography-index-[0-9]+">'
        + htmlbibitem("1", "Akkerdju")
        + htmlbibitem("2", "Bro")
        + htmlbibitem("3", "Chap")
        + htmlbibitem("4", "Dude")
        + '.*</p>',
        output, re.MULTILINE | re.DOTALL)
    # wait to ensure different timestamp
    time.sleep(0.1)
    shutil.copyfile((app.srcdir / 'test_new.bib'), (app.srcdir / 'test.bib'))
    app = make_app(*args, **kwargs)
    app.build()
    output = (app.outdir / "index.html").read_text()
    assert re.search(
        '<p id="bibtex-bibliography-index-[0-9]+">'
        + htmlbibitem("1", "Eminence")
        + htmlbibitem("2", "Frater")
        + htmlbibitem("3", "Giggles")
        + htmlbibitem("4", "Handy")
        + '.*</p>',
        output, re.MULTILINE | re.DOTALL)
