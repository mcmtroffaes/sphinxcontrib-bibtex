"""
    test_filter
    ~~~~~~~~~~~

    Test filter option.
"""

import pytest


@pytest.mark.sphinx('html', testroot='filter')
def test_filter(app, warning):
    app.builder.build_all()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text()
    assert 'Tralalala' in output
    assert 'ideetje' not in output
    assert 'Jakkamakka' not in output
    output = (app.outdir / "or.html").read_text()
    assert 'Tralalala' not in output
    assert 'ideetje' in output
    assert 'Jakkamakka' in output
    output = (app.outdir / "noteq.html").read_text()
    assert 'Tralalala' in output
    assert 'ideetje' in output
    assert 'Jakkamakka' not in output
    output = (app.outdir / "lt.html").read_text()
    assert 'Tralalala' in output
    assert 'ideetje' not in output
    assert 'Jakkamakka' not in output
    output = (app.outdir / "lte.html").read_text()
    assert 'Tralalala' in output
    assert 'ideetje' not in output
    assert 'Jakkamakka' in output
    output = (app.outdir / "gt.html").read_text()
    assert 'Tralalala' not in output
    assert 'ideetje' in output
    assert 'Jakkamakka' not in output
    output = (app.outdir / "gte.html").read_text()
    assert 'Tralalala' not in output
    assert 'ideetje' in output
    assert 'Jakkamakka' in output
    output = (app.outdir / "key.html").read_text()
    assert 'Tralalala' not in output
    assert 'ideetje' in output
    assert 'Jakkamakka' not in output
    output = (app.outdir / "false.html").read_text()
    assert 'Tralalala' not in output
    assert 'ideetje' not in output
    assert 'Jakkamakka' not in output
    output = (app.outdir / "true.html").read_text()
    assert 'Tralalala' in output
    assert 'ideetje' in output
    assert 'Jakkamakka' in output
    output = (app.outdir / "title.html").read_text()
    assert 'Tralalala' not in output
    assert 'ideetje' not in output
    assert 'Jakkamakka' in output
