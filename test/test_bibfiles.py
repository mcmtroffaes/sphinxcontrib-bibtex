import pytest
import re
import shutil
from sphinx.errors import ExtensionError
import time


status_not_found = "checking for.*in bibtex cache.*not found"
status_up_to_date = "checking for.*in bibtex cache.*up to date"
status_out_of_date = "checking for.*in bibtex cache.*out of date"
status_parsing = "parsing bibtex file.*parsed [0-9]+ entries"


def htmlbibitem(label, text):
    return (
        r'.*<dt class="label".*><span class="brackets">'
        r'*{0}.*</span></dt>\s*<dd>.*{1}.*</dd>'.format(label, text))


# Test that updates to the bibfile generate the correct result when
# Sphinx is run again.
@pytest.mark.sphinx('html', testroot='bibfiles_out_of_date')
def test_bibfiles_out_of_date(make_app, app_params):
    args, kwargs = app_params
    app = make_app(*args, **kwargs)
    app.build()
    status = app._status.getvalue()
    # not found, parsing
    assert re.search(status_not_found, status) is not None
    assert re.search(status_up_to_date, status) is None
    assert re.search(status_out_of_date, status) is None
    assert re.search(status_parsing, status) is not None
    output = (app.outdir / "index.html").read_text()
    assert re.search(
        '<p id="bibtex-bibliography-index-[0-9]+">'
        + htmlbibitem("1", "Akkerdju")
        + htmlbibitem("2", "Bro")
        + htmlbibitem("3", "Chap")
        + htmlbibitem("4", "Dude")
        + '.*</p>',
        output, re.MULTILINE | re.DOTALL) is not None
    # wait to ensure different timestamp
    time.sleep(0.1)
    shutil.copyfile((app.srcdir / 'test_new.xxx'), (app.srcdir / 'test.bib'))
    app = make_app(*args, **kwargs)
    app.build()
    status = app._status.getvalue()
    # out of date, parsing
    assert re.search(status_not_found, status) is None
    assert re.search(status_up_to_date, status) is None
    assert re.search(status_out_of_date, status) is not None
    assert re.search(status_parsing, status) is not None
    output = (app.outdir / "index.html").read_text()
    assert re.search(
        '<p id="bibtex-bibliography-index-[0-9]+">'
        + htmlbibitem("1", "Eminence")
        + htmlbibitem("2", "Frater")
        + htmlbibitem("3", "Giggles")
        + htmlbibitem("4", "Handy")
        + '.*</p>',
        output, re.MULTILINE | re.DOTALL) is not None
    # wait to ensure different timestamp
    time.sleep(0.1)
    shutil.copyfile((app.srcdir / 'index_new.xxx'), (app.srcdir / 'index.rst'))
    app = make_app(*args, **kwargs)
    app.build()
    status = app._status.getvalue()
    # up to date
    assert re.search(status_not_found, status) is None
    assert re.search(status_up_to_date, status) is not None
    assert re.search(status_out_of_date, status) is None
    assert re.search(status_parsing, status) is None


@pytest.mark.sphinx('html', testroot='bibfiles_not_found')
def test_bibfiles_not_found(app, warning):
    app.build()
    warning.seek(0)
    warnings = warning.readlines()
    assert len(warnings) == 1
    assert 'could not open bibtex file' in warnings[0]


@pytest.mark.sphinx('html', testroot='bibfiles_missing_conf')
def test_bibfiles_missing_conf(make_app, app_params):
    args, kwargs = app_params
    with pytest.raises(ExtensionError):
        make_app(*args, **kwargs)
