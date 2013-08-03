# -*- coding: utf-8 -*-
"""
    test_bibfile_out_of_date
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Test that updates to the bibfile generate the correct result when
    Sphinx is run again.
"""

import os.path
import shutil
import re
import time

from util import path, with_app

srcdir = path(__file__).parent.joinpath('bibfile_out_of_date').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)
    os.remove(srcdir / 'test.bib')


@with_app(srcdir=srcdir, warningiserror=True)
def test_encoding(app):
    shutil.copyfile(
        os.path.join(srcdir, 'test_old.bib'),
        os.path.join(srcdir, 'test.bib'))
    app.builder.build_all()
    with open(os.path.join(app.outdir, "index.html")) as stream:
        assert re.search(
            '<p id="bibtex-bibliography-index-0">'
            '.*<tr><td class="label">\\[1\\]</td><td>.*Akkerdju.*</td></tr>'
            '.*<tr><td class="label">\\[2\\]</td><td>.*Bro.*</td></tr>'
            '.*<tr><td class="label">\\[3\\]</td><td>.*Chap.*</td></tr>'
            '.*<tr><td class="label">\\[4\\]</td><td>.*Dude.*</td></tr>'
            '.*</p>',
            stream.read(), re.MULTILINE | re.DOTALL)
    # wait to ensure different timestamp
    time.sleep(0.1)
    shutil.copyfile(
        os.path.join(srcdir, 'test_new.bib'),
        os.path.join(srcdir, 'test.bib'))
    app.builder.build_all()
    with open(os.path.join(app.outdir, "index.html")) as stream:
        assert re.search(
            '<p id="bibtex-bibliography-index-0">'
            '.*<tr><td class="label">\\[1\\]</td><td>.*Eminence.*</td></tr>'
            '.*<tr><td class="label">\\[2\\]</td><td>.*Frater.*</td></tr>'
            '.*<tr><td class="label">\\[3\\]</td><td>.*Giggles.*</td></tr>'
            '.*<tr><td class="label">\\[4\\]</td><td>.*Handy.*</td></tr>'
            '.*</p>',
            stream.read(), re.MULTILINE | re.DOTALL)
