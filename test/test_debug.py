"""Some tests purely used for stepping into the debugger
to help understand what docutils/sphinx are doing.
"""

import pytest


docutils_citation_xml = """
    <paragraph>
        <reference ids="id1" internal="True" refid="label">
            <inline>
                [Label]
    <citation backrefs="id1" docname="index" ids="label" names="label">
        <label support_smartquotes="False">
            Label
        <paragraph>
            The title.
"""

bibtex_citation_xml = """
    <paragraph>
        <inline ids="id1">
            [
            <reference internal="True" refid="id3">
                <inline>
                    tes
            ]
    <paragraph ids="id2">
        <citation backrefs="id1" docname="index" ids="id3">
            <label support_smartquotes="False">
                tes
            <paragraph>
                The title.
"""


@pytest.mark.sphinx('pseudoxml', testroot='debug_docutils_citation')
def test_debug_docutils_citation(app, warning):
    """A simple test with a single standard docutils citation."""
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.pseudoxml").read_text()
    assert output.split('\n')[1:] == docutils_citation_xml.split('\n')[1:]


@pytest.mark.sphinx('pseudoxml', testroot='debug_bibtex_citation')
def test_debug_bibtex_citation(app, warning):
    """A simple test with a single standard docutils citation."""
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.pseudoxml").read_text()
    assert output.split('\n')[1:] == bibtex_citation_xml.split('\n')[1:]


# see issue 226
@pytest.mark.sphinx('pseudoxml', testroot='debug_bibtex_citation')
def test_rebuild_empty_outdir(make_app, app_params):
    args, kwargs = app_params
    app0 = make_app(freshenv=True, *args, **kwargs)
    app0.build()
    assert not app0._warning.getvalue()
    app0.outdir.rmtree()
    app1 = make_app(freshenv=False, *args, **kwargs)
    app1.build()
    assert 'could not find bibtex key' not in app1._warning.getvalue()
