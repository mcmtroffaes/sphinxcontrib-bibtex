import pytest
import sphinx


@pytest.mark.skipif(
    sphinx.version_info < (4, 0),
    reason="root_doc only supported in sphinx 4.0 and higher",
)
@pytest.mark.sphinx("pseudoxml", testroot="root_doc")
def test_root_doc(app, warning):
    app.build()
    assert not warning.getvalue()
    assert (app.outdir / "root.pseudoxml").exists()
