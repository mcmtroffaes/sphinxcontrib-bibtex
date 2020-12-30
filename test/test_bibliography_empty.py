import pytest


@pytest.mark.sphinx('html', testroot='bibliography_empty', freshenv=True)
def test_bibliography_empty_works(app, warning):
    app.build()
    assert not warning.getvalue()


@pytest.mark.sphinx(
    'pseudoxml', testroot='bibliography_empty', freshenv=True, confoverrides={
        'bibtex_bibliography_header': '.. rubric:: Regular Citations',
        'bibtex_footbibliography_header': '.. rubric:: Footnote Citations'})
def test_bibliography_empty_no_header(app, warning):
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.pseudoxml").read_text(encoding='utf-8')
    assert 'Regular Citations' not in output
    assert 'Footnote Citations' not in output
    assert '<rubric' not in output
    assert output.count('<target') == 2
