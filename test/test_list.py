from test.common import html_citations
import pytest
import re


@pytest.mark.sphinx('html', testroot='list_citation')
def test_list_citation(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text()
    assert html_citations(label='1', text='.*Akkerdju.*').search(output)
    assert html_citations(label='2', text='.*Bro.*').search(output)
    assert html_citations(label='3', text='.*Chap.*').search(output)
    assert html_citations(label='4', text='.*Dude.*').search(output)


@pytest.mark.sphinx('html', testroot='list_bullet')
def test_list_bullet(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text()
    assert re.search(
        '<ul'
        '.*<li.*Akkerdju.*</li>'
        '.*<li.*Bro.*</li>'
        '.*<li.*Chap.*</li>'
        '.*<li.*Dude.*</li>'
        '.*</ul>',
        output, re.DOTALL)


@pytest.mark.sphinx('html', testroot='list_enumerated')
def test_list_enumerated(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text()
    assert re.search(
        '<ol .*start="1".*>'
        '.*<li.*Akkerdju.*</li>'
        '.*<li.*Bro.*</li>'
        '.*<li.*Chap.*</li>'
        '.*<li.*Dude.*</li>'
        '.*</ol>'
        '.*<ol .*start="5".*>'
        '.*<li.*Eminence.*</li>'
        '.*<li.*Frater.*</li>'
        '.*<li.*Giggles.*</li>'
        '.*<li.*Handy.*</li>'
        '.*</ol>'
        '.*<ol .*start="23".*>'
        '.*<li.*Iedereen.*</li>'
        '.*<li.*Joke.*</li>'
        '.*<li.*Klopgeest.*</li>'
        '.*<li.*Laterfanter.*</li>'
        '.*</ol>',
        output, re.DOTALL)


@pytest.mark.sphinx('html', testroot='list_invalid')
def test_list_invalid(app, warning) -> None:
    app.build()
    assert re.search(
        "unknown bibliography list type 'thisisintentionallyinvalid'",
        warning.getvalue())
