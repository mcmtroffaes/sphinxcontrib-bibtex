# -*- coding: utf-8 -*-
"""
    test_autodoc
    ~~~~~~~~~~~~

    Test with autodoc.
"""

import os.path
import re
from sphinx_testing.util import path, with_app

srcdir = path(__file__).dirname().joinpath('autodoc').abspath()


def teardown_module():
    (srcdir / '_build').rmtree(True)


@with_app(srcdir=srcdir, warningiserror=True)
def test_autodoc(app, status, warning):
    app.builder.build_all()
    with open(os.path.join(app.outdir, "doc_cite.html")) as stream:
        output = stream.read()
        assert len(re.findall("\\[One\\]", output)) == 1
        assert len(re.findall("\\[Two\\]", output)) == 1
        assert len(re.findall("\\[Thr\\]", output)) == 1
        assert len(re.findall("\\[Fou\\]", output)) == 1
        assert len(re.findall("\\[Fiv\\]", output)) == 1
        assert len(re.findall("\\[Six\\]", output)) == 1
        assert len(re.findall("\\[Sev\\]", output)) == 1
        assert len(re.findall("\\[Eig\\]", output)) == 1
        assert len(re.findall("\\[Nin\\]", output)) == 1
        assert len(re.findall("Een", output)) == 1
        assert len(re.findall("Twee", output)) == 1
        assert len(re.findall("Drie", output)) == 1
        assert len(re.findall("Vier", output)) == 1
        assert len(re.findall("Vijf", output)) == 1
        assert len(re.findall("Zes", output)) == 1
        assert len(re.findall("Zeven", output)) == 1
        assert len(re.findall("Acht", output)) == 1
        assert len(re.findall("Negen", output)) == 1
    with open(os.path.join(app.outdir, "doc_footcite.html")) as stream:
        output = stream.read()
        assert len(re.findall(">1<", output)) == 2
        assert len(re.findall(">2<", output)) == 2
        assert len(re.findall(">3<", output)) == 2
        assert len(re.findall(">4<", output)) == 2
        assert len(re.findall(">5<", output)) == 2
        assert len(re.findall(">6<", output)) == 2
        assert len(re.findall(">7<", output)) == 2
        assert len(re.findall(">8<", output)) == 2
        assert len(re.findall(">9<", output)) == 2
        assert len(re.findall("Een", output)) == 1
        assert len(re.findall("Twee", output)) == 1
        assert len(re.findall("Drie", output)) == 1
        assert len(re.findall("Vier", output)) == 1
        assert len(re.findall("Vijf", output)) == 1
        assert len(re.findall("Zes", output)) == 1
        assert len(re.findall("Zeven", output)) == 1
        assert len(re.findall("Acht", output)) == 1
        assert len(re.findall("Negen", output)) == 1
