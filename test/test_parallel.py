"""Test for parallel build."""

import os

import pytest
from sphinx.util.parallel import parallel_available


@pytest.mark.skipif(
    not parallel_available, reason="sphinx parallel builds not available"
)
@pytest.mark.sphinx("html", testroot="parallel")
def test_parallel(make_app, app_params) -> None:
    args, kwargs = app_params
    app0 = make_app(*args, **kwargs)
    app0.parallel = 4
    app0.build()
    assert not app0._warning.getvalue()
    # update files to trigger merge of citations domain data
    docnames = {
        "{0}/doc{1:02d}".format(folder, i)
        for i in (1, 3, 5, 7, 11, 15, 19)
        for folder in ("regular", "foot")
    }
    for docname in docnames:
        rstname = app0.env.doc2path(docname)
        htmlname = app0.builder.get_outfilename(docname)
        mtime = (app0.builder.outdir / htmlname).stat().st_mtime
        os.utime(app0.srcdir / rstname, (mtime + 5, mtime + 5))
    updated = set(app0.builder.get_outdated_docs())
    assert updated == docnames
    app1 = make_app(*args, **kwargs)
    app1._warning.seek(0)
    app1._warning.truncate()
    app1.build()
    assert not app1._warning.getvalue()
