# -*- coding: utf-8 -*-
"""
    test_autodoc
    ~~~~~~~~~~~~

    Test with autodoc.
"""

import pytest
import re


@pytest.mark.sphinx('html', testroot='autodoc')
def test_autodoc(app, warning):
    app.builder.build_all()
    assert not warning.getvalue()
    output = (app.outdir / "doc_cite.html").read_text()
    assert len(re.findall("\\[One\\]", output)) == 1
    assert len(re.findall("\\[Two\\]", output)) == 1
    assert len(re.findall("\\[Thr\\]", output)) == 1
    assert len(re.findall("\\[Fou\\]", output)) == 1
    assert len(re.findall("\\[Fiv\\]", output)) == 1
    assert len(re.findall("\\[Six\\]", output)) == 1
    assert len(re.findall("\\[Sev\\]", output)) == 1
    assert len(re.findall("\\[Eig\\]", output)) == 1
    assert len(re.findall("\\[Nin\\]", output)) == 1
    assert len(re.findall("\\[Ten\\]", output)) == 1
    assert len(re.findall("\\[Ele\\]", output)) == 1
    assert len(re.findall("Een", output)) == 1
    assert len(re.findall("Twee", output)) == 1
    assert len(re.findall("Drie", output)) == 1
    assert len(re.findall("Vier", output)) == 1
    assert len(re.findall("Vijf", output)) == 1
    assert len(re.findall("Zes", output)) == 1
    assert len(re.findall("Zeven", output)) == 1
    assert len(re.findall("Acht", output)) == 1
    assert len(re.findall("Negen", output)) == 1
    assert len(re.findall("Tien", output)) == 1
    assert len(re.findall("Elf", output)) == 1
    output2 = (app.outdir / "doc_footcite.html").read_text()
    assert len(re.findall(">1<", output2)) == 2
    assert len(re.findall(">2<", output2)) == 2
    assert len(re.findall(">3<", output2)) == 2
    assert len(re.findall(">4<", output2)) == 2
    assert len(re.findall(">5<", output2)) == 2
    assert len(re.findall(">6<", output2)) == 2
    assert len(re.findall(">7<", output2)) == 2
    assert len(re.findall(">8<", output2)) == 2
    assert len(re.findall(">9<", output2)) == 2
    assert len(re.findall(">10<", output2)) == 2
    assert len(re.findall(">11<", output2)) == 2
    assert len(re.findall("Een", output2)) == 1
    assert len(re.findall("Twee", output2)) == 1
    assert len(re.findall("Drie", output2)) == 1
    assert len(re.findall("Vier", output2)) == 1
    assert len(re.findall("Vijf", output2)) == 1
    assert len(re.findall("Zes", output2)) == 1
    assert len(re.findall("Zeven", output2)) == 1
    assert len(re.findall("Acht", output2)) == 1
    assert len(re.findall("Negen", output2)) == 1
    assert len(re.findall("Tien", output2)) == 1
    assert len(re.findall("Elf", output2)) == 1
