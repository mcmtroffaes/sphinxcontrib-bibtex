"""Test warnings on duplicate labels/keys."""

import pytest
import re


def htmlbiblabel(label):
    return (
        r'<dt class="label".*><span class="brackets">{0}</span>'
        .format(label))


@pytest.mark.sphinx('html', testroot='duplicate_label')
def test_duplicate_label(app, warning):
    # see github issue 14
    app.builder.build_all()
    assert re.search(
        r"duplicate label 1 for keys ({'Test', 'Test2'})|({'Test2', 'Test'})",
        warning.getvalue())
    output = (app.outdir / "doc1.html").read_text()
    assert re.search(htmlbiblabel("1"), output)
    output = (app.outdir / "doc2.html").read_text()
    assert re.search(htmlbiblabel("1"), output)


@pytest.mark.sphinx('html', testroot='duplicate_citation')
def test_duplicate_citation(app, warning):
    app.builder.build_all()
    warning.seek(0)
    warnings = list(warning.readlines())
    assert len(warnings) == 1
    assert "duplicate citation for key Test" in warnings[0]
    # assure there's only one id for this citation
    output = (app.outdir / "index.html").read_text()
    assert output.count('id="bibtex-citation-test"') == 1


@pytest.mark.sphinx('html', testroot='duplicate_nearly_identical_keys')
def test_duplicate_nearly_identical_keys(app, warning):
    app.builder.build_all()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text()
    # assure both citations and citation references are present
    assert "[Smi]" in output
    assert "Smith" in output
    assert "[Pop]" in output
    assert "Poppins" in output
    assert "[Ein]" in output
    assert "Einstein" in output
    # assure distinct ids for citations
    assert output.count('id="bibtex-citation-test"') == 1
    assert output.count('id="bibtex-citation-test1"') == 1
    assert output.count('id="bibtex-citation-test2"') == 1
