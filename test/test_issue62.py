# -*- coding: utf-8 -*-
"""
    test_issue62
    ~~~~~~~~~~~~

    Test local bibliographies.
"""

import pytest
import re


def extract_references(code):
    return frozenset(re.findall(
        '<a class="bibtex reference internal" href="([^"]+)"', code))


def extract_citations(code):
    return frozenset(re.findall(
        '<dt class="bibtex label" id="([^"]+)"', code))


def check_code(code, refs, cites, otherrefs, othercites):
    code_refs = extract_references(code)
    code_cites = extract_citations(code)
    # use <= here because refs contains all internal references, not
    # just citation references
    assert refs <= code_refs
    assert cites == code_cites
    assert not(otherrefs & code_refs)
    assert not(othercites & code_cites)


@pytest.mark.sphinx('html', testroot='issue62')
def test_local_bibliographies(app, warning):
    doc1_refs = frozenset([
        '#wustner-atomistic-2014',
        '#fuhrmans-molecular-2012',
        '#blume-apparent-1983',
        '#grabitz-relaxation-2002',
        ])
    doc1_cites = frozenset([
        'blume-apparent-1983',
        'wustner-atomistic-2014',
        'fuhrmans-molecular-2012',
        'grabitz-relaxation-2002'
        ])
    doc2_refs = frozenset([
        '#shirts-simple-2013'
        ])
    doc2_cites = frozenset([
        'shirts-simple-2013'
        ])
    sum_refs = frozenset([
        "#mcmahon-membrane-2010",
        "#hu-gaussian-2013",
        "doc1.html#fuhrmans-molecular-2012",
        "#risselada-curvature-dependent-2011",
        "#risselada-curvature-2009",
        "#marrink-mechanism-2003",
        ])
    sum_cites = frozenset([
        'hu-gaussian-2013',
        'marrink-mechanism-2003',
        'risselada-curvature-2009',
        'risselada-curvature-dependent-2011',
        'mcmahon-membrane-2010',
        ])
    app.builder.build_all()
    assert not warning.getvalue()
    output = (app.outdir / "doc1.html").read_text(encoding='utf-8')
    check_code(output, doc1_refs, doc1_cites,
               doc2_refs | sum_refs, doc2_cites | sum_cites)
    output = (app.outdir / "doc2.html").read_text(encoding='utf-8')
    check_code(output, doc2_refs, doc2_cites,
               doc1_refs | sum_refs, doc1_cites | sum_cites)
    output = (app.outdir / "summary.html").read_text(encoding='utf-8')
    check_code(output, sum_refs, sum_cites,
               doc1_refs | doc2_refs, doc1_cites | doc2_cites)
