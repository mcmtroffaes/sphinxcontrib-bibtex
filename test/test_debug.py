"""Some tests purely used for stepping into the debugger
to help understand what docutils/sphinx are doing.
"""

import shutil

import docutils
import pytest

docutils_citation_xml = """
    <paragraph>
        <reference ids="id1" internal="1" refid="label">
            <inline>
                [Label]
    <citation backrefs="id1" docname="index" ids="label" names="label">
        <label support_smartquotes="0">
            Label
        <paragraph>
            The title.
"""

bibtex_citation_xml = """
    <paragraph>
        <inline classes="bibtex-citation" ids="id1">
            [
            <reference internal="1" refid="id3" reftitle="The title.">
                tes
            ]
    <container ids="id2">
        <citation backrefs="id1" docname="index" ids="id3">
            <label support_smartquotes="0">
                tes
            <paragraph>
                The title.
"""

if docutils.__version_info__ < (0, 22):
    docutils_citation_xml = docutils_citation_xml.replace('="1"', '="True"')
    docutils_citation_xml = docutils_citation_xml.replace('="0"', '="False"')
    bibtex_citation_xml = bibtex_citation_xml.replace('="1"', '="True"')
    bibtex_citation_xml = bibtex_citation_xml.replace('="0"', '="False"')


@pytest.mark.sphinx("pseudoxml", testroot="debug_docutils_citation")
def test_debug_docutils_citation(app, warning):
    """A simple test with a single standard docutils citation."""
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.pseudoxml").read_text()
    assert output.split("\n")[1:] == docutils_citation_xml.split("\n")[1:]


@pytest.mark.sphinx("pseudoxml", testroot="debug_bibtex_citation")
def test_debug_bibtex_citation(app, warning):
    """A simple test with a single standard docutils citation."""
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.pseudoxml").read_text()
    assert output.split("\n")[1:] == bibtex_citation_xml.split("\n")[1:]


# see issue 226
@pytest.mark.sphinx("pseudoxml", testroot="debug_bibtex_citation")
def test_rebuild_empty_outdir(make_app, app_params):
    args, kwargs = app_params
    app0 = make_app(freshenv=True, *args, **kwargs)
    app0.build()
    assert not app0._warning.getvalue()
    shutil.rmtree(app0.outdir)
    app1 = make_app(freshenv=False, *args, **kwargs)
    app1.build()
    assert "could not find bibtex key" not in app1._warning.getvalue()


@pytest.mark.sphinx("pseudoxml", testroot="debug_minimal_example")
def test_debug_minimal_example(app, warning) -> None:
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.pseudoxml").read_text()
    docutils_0_22 = docutils.__version_info__ >= (0, 22)
    assert list(output.split("\n"))[1:] == [
        "    <paragraph>",
        "        See ",
        '        <inline classes="bibtex-citation" ids="id1">',
        "            Nelson [",
        f'            <reference internal="{1 if docutils_0_22 else True}" refid="id4" '
        'reftitle="Edward Nelson. Radically Elementary Probability Theory. '
        'Princeton University Press, 1987.">',
        "                Nel87",
        "            ]",
        "         for an introduction to non-standard analysis.",
        "        Non-standard analysis is fun ",
        '        <inline classes="bibtex-citation" ids="id2">',
        "            [",
        f'            <reference internal="{1 if docutils_0_22 else True}" refid="id4" '
        'reftitle="Edward Nelson. Radically Elementary Probability Theory. '
        'Princeton University Press, 1987.">',
        "                Nel87",
        "            ]",
        "        .",
        '    <container ids="id3">',
        '        <citation backrefs="id1 id2" docname="index" ids="id4">',
        f'            <label support_smartquotes="{0 if docutils_0_22 else False}">',
        "                Nel87",
        "            <paragraph>",
        "                Edward Nelson.",
        "                 ",
        "                <emphasis>",
        "                    Radically Elementary Probability Theory",
        "                .",
        "                 ",
        "                Princeton University Press, 1987.",
        "",
    ]
