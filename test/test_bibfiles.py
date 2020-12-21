import pytest
import re
import shutil
from sphinx.errors import ExtensionError
import time


def htmlbibitem(label, text):
    return (
        '.*<dt class="bibtex label".*><span class="brackets">'
        '<a.*>{0}</a></span></dt>\\s*<dd>.*{1}.*</dd>'.format(label, text))

# Test that updates to the bibfile generate the correct result when
# Sphinx is run again.
@pytest.mark.sphinx('html', testroot='bibfiles_out_of_date')
def test_bibfiles_out_of_date(make_app, app_params, warning):
    args, kwargs = app_params
    app = make_app(*args, **kwargs)
    app.build()
    output = (app.outdir / "index.html").read_text()
    assert re.search(
        '<p id="bibtex-bibliography-index-[0-9]+">'
        + htmlbibitem("1", "Akkerdju")
        + htmlbibitem("2", "Bro")
        + htmlbibitem("3", "Chap")
        + htmlbibitem("4", "Dude")
        + '.*</p>',
        output, re.MULTILINE | re.DOTALL)
    # wait to ensure different timestamp
    time.sleep(0.1)
    shutil.copyfile((app.srcdir / 'test_new.bib'), (app.srcdir / 'test.bib'))
    app = make_app(*args, **kwargs)
    app.build()
    output = (app.outdir / "index.html").read_text()
    assert re.search(
        '<p id="bibtex-bibliography-index-[0-9]+">'
        + htmlbibitem("1", "Eminence")
        + htmlbibitem("2", "Frater")
        + htmlbibitem("3", "Giggles")
        + htmlbibitem("4", "Handy")
        + '.*</p>',
        output, re.MULTILINE | re.DOTALL)


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
