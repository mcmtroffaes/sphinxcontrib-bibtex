import os
import re
import subprocess
import sys

import pytest

from test.common import html_citations

TITLES = {
    "conditional": "Conditional Entry",
    "visible": "Visible Entry",
    "nested": "Nested Entry",
    "negative": "Negative Entry",
    "unused": "Unused Entry",
}


def make_source(srcdir, cross_document):
    srcdir.mkdir()
    (srcdir / "conf.py").write_text(
        "extensions = ['sphinxcontrib.bibtex']\n"
        "bibtex_bibfiles = ['refs.bib']\n"
        "bibtex_default_style = 'unsrt'\n",
        encoding="utf-8",
    )
    (srcdir / "refs.bib").write_text(
        "\n".join(
            f"@book{{{key}, author={{A. Author}}, title={{{{{title}}}}}, "
            "publisher={Publisher}, year={2024}}"
            for key, title in TITLES.items()
        ),
        encoding="utf-8",
    )
    references = """Conditional citations
=====================

.. only:: alpha

   Conditional :cite:p:`conditional`, shared :cite:p:`visible`.

.. only:: html

   Visible :cite:p:`visible`.

.. only:: alpha

   .. only:: beta

      Nested :cite:p:`nested`.

.. only:: not alpha

   Negative :cite:p:`negative`.

.. only:: latex

   Hidden :cite:p:`unused`.

"""
    bibliographies = """Cited
-----

.. bibliography::
   :cited:

All
---

.. bibliography::
   :all:
   :list: bullet

Not cited
---------

.. bibliography::
   :notcited:
   :list: bullet
"""
    if cross_document:
        references += ".. toctree::\n\n   bibliography\n"
        (srcdir / "bibliography.rst").write_text(
            "Bibliographies\n==============\n\n" + bibliographies,
            encoding="utf-8",
        )
    else:
        references += bibliographies
    (srcdir / "index.rst").write_text(references, encoding="utf-8")


def build(srcdir, outdir, tags, parallel=1):
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "sphinx",
            "-b",
            "html",
            "-a",
            "-W",
            "-j",
            str(parallel),
            *(arg for tag in tags for arg in ("-t", tag)),
            str(srcdir),
            str(outdir),
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env={**os.environ, "PYTHONUTF8": "1"},
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return result.stdout


def check_output(outdir, cross_document, tags):
    page = outdir / ("bibliography.html" if cross_document else "index.html")
    output = page.read_text(encoding="utf-8")
    sections = {
        name: re.search(rf'<section id="{name}">(.*?)</section>', output, re.S)[1]
        for name in ("cited", "all", "not-cited")
    }
    active = (["conditional"] if "alpha" in tags else []) + ["visible"]
    if "alpha" in tags and "beta" in tags:
        active.append("nested")
    if "alpha" not in tags:
        active.append("negative")
    expected = {
        "cited": set(active),
        "all": set(TITLES),
        "not-cited": set(TITLES) - set(active),
    }
    for name, section in sections.items():
        actual = {key for key, title in TITLES.items() if title in section}
        assert actual == expected[name]
    citations = list(html_citations().finditer(sections["cited"]))
    assert [match["label"] for match in citations] == [
        str(number) for number in range(1, len(active) + 1)
    ]
    assert [
        next(key for key in active if TITLES[key] in match["text"])
        for match in citations
    ] == active
    if not cross_document:
        targets = set(re.findall(r'\bid="([^"]+)"', output))
        backrefs = re.findall(r'role="doc-backlink" href="#([^"]+)"', output)
        assert backrefs and set(backrefs) <= targets


@pytest.mark.parametrize("cross_document", [False, True])
@pytest.mark.parametrize("tags", [[], ["alpha"], ["beta"], ["alpha", "beta"]])
def test_only_citations(tmp_path, cross_document, tags):
    srcdir, outdir = tmp_path / "source", tmp_path / "html"
    make_source(srcdir, cross_document)
    build(srcdir, outdir, tags)
    check_output(outdir, cross_document, tags)


@pytest.mark.parametrize("cross_document", [False, True])
def test_only_citations_incremental(tmp_path, cross_document):
    srcdir, outdir = tmp_path / "source", tmp_path / "html"
    make_source(srcdir, cross_document)
    build(srcdir, outdir, [])
    check_output(outdir, cross_document, [])
    doctree = outdir / ".doctrees" / "index.doctree"
    initial_mtime = doctree.stat().st_mtime_ns
    for tags in (["alpha", "beta"], []):
        build(srcdir, outdir, tags)
        check_output(outdir, cross_document, tags)
        assert doctree.stat().st_mtime_ns == initial_mtime


def test_only_missing_key(tmp_path):
    srcdir, outdir = tmp_path / "source", tmp_path / "html"
    make_source(srcdir, False)
    index = srcdir / "index.rst"
    index.write_text(
        index.read_text(encoding="utf-8").replace("`unused`", "`missing`"),
        encoding="utf-8",
    )
    build(srcdir, outdir, [])


def test_invalid_only_expression_keeps_warning(tmp_path):
    srcdir, outdir = tmp_path / "source", tmp_path / "html"
    make_source(srcdir, False)
    index = srcdir / "index.rst"
    index.write_text(
        index.read_text(encoding="utf-8").replace(
            ".. only:: alpha\n", ".. only:: alpha +\n", 1
        ),
        encoding="utf-8",
    )
    with pytest.raises(
        AssertionError, match="exception while evaluating only directive expression"
    ):
        build(srcdir, outdir, [])
    output = (outdir / "index.html").read_text(encoding="utf-8")
    cited = re.search(r'<section id="cited">(.*?)</section>', output, re.S)[1]
    assert "Conditional Entry" in cited


@pytest.mark.skipif(
    sys.platform == "win32", reason="Sphinx parallel reading needs fork"
)
def test_only_citations_parallel_merge_and_purge(tmp_path):
    srcdir, outdir = tmp_path / "source", tmp_path / "html"
    make_source(srcdir, True)
    index = srcdir / "index.rst"
    index.write_text(
        index.read_text(encoding="utf-8")
        + "".join(f"   extra{number}\n" for number in range(6)),
        encoding="utf-8",
    )
    for number in range(6):
        key = "unused" if number == 0 else "visible"
        (srcdir / f"extra{number}.rst").write_text(
            f"Extra {number}\n=======\n\n.. only:: alpha\n\n"
            f"   Extra citation :cite:p:`{key}`.\n",
            encoding="utf-8",
        )
    pids = tmp_path / "reader-pids.txt"
    with (srcdir / "conf.py").open("a", encoding="utf-8") as conf:
        conf.write(
            "import os\n"
            "def record_reader(app, doctree):\n"
            f"    with open({str(pids)!r}, 'a') as stream:\n"
            "        stream.write(str(os.getpid()) + '\\n')\n"
            "def setup(app):\n"
            "    app.connect('doctree-read', record_reader)\n"
        )
    build(srcdir, outdir, ["alpha", "beta"], parallel=2)
    assert len(set(pids.read_text().splitlines())) > 1
    output = (outdir / "bibliography.html").read_text(encoding="utf-8")
    cited = re.search(r'<section id="cited">(.*?)</section>', output, re.S)[1]
    assert "Unused Entry" in cited
    (srcdir / "extra0.rst").unlink()
    index.write_text(
        index.read_text(encoding="utf-8").replace("   extra0\n", ""),
        encoding="utf-8",
    )
    build(srcdir, outdir, ["alpha", "beta"], parallel=2)
    check_output(outdir, True, ["alpha", "beta"])
