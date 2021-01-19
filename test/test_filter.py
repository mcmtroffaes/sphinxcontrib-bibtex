import pytest


@pytest.mark.sphinx('html', testroot='filter')
def test_filter(app, warning) -> None:
    app.build()
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


@pytest.mark.sphinx('html', testroot='filter_fix_author_keyerror')
def test_filter_fix_author_keyerror(app) -> None:
    app.build()


@pytest.mark.sphinx('html', testroot='filter_option_clash')
def test_filter_option_clash(app, warning) -> None:
    app.build()
    warnings = warning.getvalue()
    assert ':filter: overrides :all:' in warnings
    assert ':filter: overrides :cited:' in warnings
    assert ':filter: overrides :notcited:' in warnings


@pytest.mark.sphinx('html', testroot='filter_syntax_error')
def test_filter_syntax_error(app, warning) -> None:
    app.build()
    assert warning.getvalue().count('syntax error in :filter: expression') == 9
