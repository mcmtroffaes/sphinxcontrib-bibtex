# -*- coding: utf-8 -*-
"""
    test_bibfile_out_of_date
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Test that updates to the bibfile generate the correct result when
    Sphinx is run again.
"""

import shutil
import re
import time
from sphinx_testing.util import path, with_app


srcdir = path(__file__).dirname().joinpath('bibfile_out_of_date').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)
    (srcdir / 'test.bib').rmtree(True)


def htmlbibitem(label, text):
    return (
        '.*<dt class="bibtex label".*><span class="brackets">'
        '<a.*>{0}</a></span></dt>\\s*<dd>.*{1}.*</dd>'.format(label, text))


@with_app(srcdir=srcdir, warningiserror=True)
def test_bibfile_out_of_date(app, status, warning):
    shutil.copyfile((srcdir / 'test_old.bib'), (srcdir / 'test.bib'))
    app.builder.build_all()
    output = (path(app.outdir) / "index.html").read_text()
    assert re.search(
        '<p id="bibtex-bibliography-index-0">'
        + htmlbibitem("1", "Akkerdju")
        + htmlbibitem("2", "Bro")
        + htmlbibitem("3", "Chap")
        + htmlbibitem("4", "Dude")
        + '.*</p>',
        output, re.MULTILINE | re.DOTALL)
    # wait to ensure different timestamp
    time.sleep(0.1)
    shutil.copyfile((srcdir / 'test_new.bib'), (srcdir / 'test.bib'))
    app.builder.build_all()
    output = (path(app.outdir) / "index.html").read_text()
    assert re.search(
        '<p id="bibtex-bibliography-index-0">'
        + htmlbibitem("1", "Eminence")
        + htmlbibitem("2", "Frater")
        + htmlbibitem("3", "Giggles")
        + htmlbibitem("4", "Handy")
        + '.*</p>',
        output, re.MULTILINE | re.DOTALL)
