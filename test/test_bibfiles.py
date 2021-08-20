from pybtex.exceptions import PybtexError

from test.common import html_citations
import pytest
import re
import shutil
from sphinx.errors import ExtensionError
import time


status_up_to_date = "checking bibtex cache.*up to date"
status_out_of_date = "checking bibtex cache.*out of date"
status_parsing = "parsing bibtex file.*parsed [0-9]+ entries"


# Test that updates to the bibfile generate the correct result when
# Sphinx is run again.
@pytest.mark.sphinx('html', testroot='bibfiles_out_of_date')
def test_bibfiles_out_of_date(make_app, app_params) -> None:
    args, kwargs = app_params
    app = make_app(*args, **kwargs)
    app.build()
    status = app._status.getvalue()
    # not found, parsing
    assert re.search(status_up_to_date, status) is None
    assert re.search(status_out_of_date, status) is not None
    assert re.search(status_parsing, status) is not None
    output = (app.outdir / "index.html").read_text()
    assert html_citations(label='1', text='.*Akkerdju.*').search(output)
    assert html_citations(label='2', text='.*Bro.*').search(output)
    assert html_citations(label='3', text='.*Chap.*').search(output)
    assert html_citations(label='4', text='.*Dude.*').search(output)
    # wait to ensure different timestamp
    time.sleep(0.1)
    shutil.copyfile((app.srcdir / 'test_new.xxx'), (app.srcdir / 'test.bib'))
    app = make_app(*args, **kwargs)
    app.build()
    status = app._status.getvalue()
    # out of date, parsing
    assert re.search(status_up_to_date, status) is None
    assert re.search(status_out_of_date, status) is not None
    assert re.search(status_parsing, status) is not None
    output = (app.outdir / "index.html").read_text()
    assert html_citations(label='1', text='.*Eminence.*').search(output)
    assert html_citations(label='2', text='.*Frater.*').search(output)
    assert html_citations(label='3', text='.*Giggles.*').search(output)
    assert html_citations(label='4', text='.*Handy.*').search(output)
    # wait to ensure different timestamp
    time.sleep(0.1)
    shutil.copyfile((app.srcdir / 'index_new.xxx'), (app.srcdir / 'index.rst'))
    app = make_app(*args, **kwargs)
    app.build()
    status = app._status.getvalue()
    # up to date
    assert re.search(status_up_to_date, status) is not None
    assert re.search(status_out_of_date, status) is None
    assert re.search(status_parsing, status) is None


@pytest.mark.sphinx('html', testroot='bibfiles_not_found')
def test_bibfiles_not_found(app, warning) -> None:
    app.build()
    warning.seek(0)
    warnings = warning.readlines()
    assert len(warnings) == 2
    assert 'could not open bibtex file' in warnings[0]
    assert 'not found or not configured in bibtex_bibfiles' in warnings[1]


@pytest.mark.sphinx('html', testroot='bibfiles_missing_conf')
def test_bibfiles_missing_conf(make_app, app_params) -> None:
    args, kwargs = app_params
    with pytest.raises(ExtensionError, match="bibtex_bibfiles"):
        make_app(*args, **kwargs)


@pytest.mark.sphinx('html', testroot='bibfiles_encoding', freshenv=True)
def test_bibfiles_encoding(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text()
    assert u"Äpplé" in output


@pytest.mark.sphinx('html', testroot='bibfiles_encoding', freshenv=True,
                    confoverrides={'bibtex_encoding': 'ascii'})
def test_bibfiles_encoding_bad(make_app, app_params) -> None:
    args, kwargs = app_params
    with pytest.raises(PybtexError, match="can't decode byte 0xc4"):
        make_app(*args, **kwargs)


@pytest.mark.sphinx('html', testroot='bibfiles_encoding', freshenv=True,
                    confoverrides={'bibtex_encoding': 'invalid'})
def test_bibfiles_encoding_invalid(make_app, app_params) -> None:
    args, kwargs = app_params
    with pytest.raises(LookupError, match="unknown encoding"):
        make_app(*args, **kwargs)


@pytest.mark.sphinx('html', testroot='bibfiles_subfolder')
def test_bibfiles_subfolder(app, warning) -> None:
    app.build()
    assert not warning.getvalue()


@pytest.mark.sphinx('html', testroot='bibfiles_multiple_macros')
def test_bibfiles_multiple_macros(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text()
    assert html_citations(
        label='1', text=r'.*Rev\. Mod\. Phys\..*').search(output)


@pytest.mark.sphinx('html', testroot='bibfiles_multiple_keys')
def test_bibfiles_multiple_keys(app, warning) -> None:
    app.build()
    assert re.search(
        "bibliography data error in .*: repeated bibliograhpy entry: test",
        warning.getvalue()) is not None
    output = (app.outdir / "index.html").read_text()
    assert html_citations(label='1', text='.*Test one.*').search(output)
