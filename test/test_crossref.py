"""
    test_crossref
    ~~~~~~~~~~~~~

    Test that cross references work.
"""

import os.path
import re

from sphinx_testing.util import path, with_app

srcdir = path(__file__).dirname().joinpath('crossref').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warningiserror=True)
def test_crossref(app, status, warning):
    app.builder.build_all()
    # default style is plain; check output
    with open(os.path.join(app.outdir, "contents.html")) as stream:
        output = stream.read()
        # ensure Zaf is cited
        assert len(re.findall('\\[Zaf\\]', output)) == 2
        # ensure proceedings only mentioned for Zaf
        assert len(re.findall(
            'Proceedings of the Second International Symposium '
            'on Imprecise Probabilities and Their Applications', output)) == 1
