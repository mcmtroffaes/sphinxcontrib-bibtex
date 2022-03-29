import pytest


@pytest.mark.sphinx('pseudoxml', testroot='root_doc')
def test_root_doc(app, warning):
    app.build()
    assert not warning.getvalue()
    assert (app.outdir / "root.pseudoxml").exists()
