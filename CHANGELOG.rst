2.6.2 (10 January 2023)
-----------------------

* Fix bibliography header repetition when recompiling documents
  (reported by ragonneau, see issue #342 and pull request #343).

2.6.1 (27 August 2023)
----------------------

* The ``:cite:alp:`` role in the super style now also suppresses the sup tag
  in addition to the brackets, to make it easier to apply the necessary formatting
  around the citation.

2.6.0 (24 August 2023)
----------------------

* Pre- and post-text in citations are now supported for the
  author_year, label, and super referencing styles. The syntax is
  ``:cite:p:`{pre-text}key{post-text}``` (requested by RobertoBagnara,
  see issue #288 and pull request #316).
  Refer to the documentation for more details.

* New alternative style citations are now supported for the
  author_year, label, and super parenthetical referencing styles,
  which are identical to parenthetical citations but without the brackets.
  The syntax is
  ``:cite:alp:`key``` (requested by davidorme, see pull request #316).
  Refer to the documentation for more details.

* Exclude docutils 0.18 and 0.19 to fix generation of a spurious div tag in the
  html builder (see issues #330, #329, #323, #322, #309).

* Add test for running the extension on Cython modules (see issue #308).

* Add test for running the extension with autoapi (see issue #319).

* Sphinx versions 2.x (and lower) are no longer supported.
  New minimum required version of Sphinx is 3.5.

* Running pytest without arguments will now by default skip all marked tests
  that require additional dependencies (currently numpydoc, rinohtype, and
  cython).

* Fix encoding issues when running tests on Windows.

* Python 3.6 is EOL and is therefore no longer officially supported.

2.5.0 (22 August 2022)
----------------------

* Add support for the rinohtype builder (reported by brechtm, see issue #275).

* Migrate from ``pkg_resources`` to ``importlib.metadata``. A side effect of
  this migration is that
  **plugins registered at runtime are longer exposed as entry points**.
  This is because ``importlib`` does not allow runtime modification of
  entry points.

* Remove sphinxcontrib namespace ``__init__.py`` file (no longer needed for
  Python 3.3+ by PEP420).

* Add support for docutils 0.18.

* Suppress LaTeX url commands in tooltips (see issue #305, reported by
  1kastner).

* Document Markdown syntax for MyST (suggested by jacopok, see issue #310).

2.4.2 (10 April 2022)
---------------------

* Add support for Python 3.10 and 3.11.

* New ``bibtex_tooltips`` option.
  Set to ``False`` to disable tooltip generation.
  See issue #286.

* New ``bibtex_tooltips_style`` option to customize tooltip text style.
  If empty (the default), the bibliography style is used.
  See issue #286.

* Support for ``root_doc`` option introduced in Sphinx 4.0
  (see issue #292, reported by jhmeinke).

* Use container node instead of paragraph node for containing bibliographies,
  fixing a violation against the docutils spec
  (see issue #273, reported by rappdw, with additional input from brechtm).

* Fix mutable dataclass fields for Python 3.11 (see issue #284 and pull
  request #285; reported and fixed by jamesjer)

* Internal refactor: embed ``reference_text_class`` directly inside the pybtex
  nodes. This enables different text classes to be used by different styles, so
  different sorts of docutils nodes can be generated on rendering depending on
  the pybtex node used. See discussion in issue #275.

* Add numpydoc regression test.

* Bump minimal pybtex requirement to 0.24.

2.4.1 (10 September 2021)
-------------------------

* Gracefully handle textual citations when author or year are missing
  (see issue #267, reported by fbkarsdorp).

2.4.0 (8 September 2021)
------------------------

* Allow specific warnings to be suppressed (see issue #255, contributed by
  stevenrhall).

* Fix parsing of LaTeX url commands in bibtex fields (see issue #258, reported
  by Matthew Giassa).

* Remove space between footnote and author for textual footnote citations in
  the default foot referencing style.

* Document how to use a backslash escaped space to suppress space before
  footnotes (see issue #256, reported by hagenw).

* Parse all bib files together, so macros specified in one file can be used in
  another file (see issue #216, reported by mforbes).
  As a consequence, duplicate citation keys across bib files will
  now also result in proper warnings.
  The ``parse_bibfile`` and ``process_bibfile`` functions have been been
  replaced by ``parse_bibdata`` and ``process_bibdata`` in the API.

* New ``bibtex_cite_id``, ``bibtex_footcite_id``,
  ``bibtex_bibliography_id``, and ``bibtex_footbibliography_id`` settings,
  which allow custom ids (which can be used as html anchors)
  to be generated for citations and bibliographies,
  based on the citation keys rather than some random numbers
  (see issue #264, reported by kmuehlbauer).
  Refer to the documentation for detailed usage and examples.

* Switch to github actions for regression testing.

* The API is now fully type checked.

* Various minor improvements in documentation and code.

2.3.0 (1 June 2021)
-------------------

* Add ``:footcite:p:`` and ``:footcite:t:`` roles.
  For capitalizing the first letter and/or listing the full author list,
  you can use ``:footcite:ct:``, ``:footcite:ts:``, ``:footcite:cts:``,
  and ``:footcite:ps:``.

* To configure your footnote referencing style,
  an optional config setting ``bibtex_foot_reference_style`` has been added.
  If not specified, this defaults to the ``foot`` style,
  which will use plain footnote references for citation references, matching
  the referencing style as in previous versions.
  Footnote reference styles can be fully customized to your heart's desire,
  similar to regular citation reference styles.

* New ``:cite:empty:`` role which registers a citation without generating
  a reference, similar to LaTeX's nocite command (see issue #131).

* Citation keys can now be listed directly under the bibliography directive,
  one key per line; such citations will always be included, regardless of
  any filter settings (see issue #54).

* A plain text preview of the full citation information will be shown when
  hovering over a citation reference
  (see issue #198, requested by eric-wieser).

* The separator between the text and the reference of all textual citation
  styles can now be customized.

2.2.1 (16 May 2021)
-------------------

* The LaTeX output now uses hyperlink instead of sphinxcite. This fixes
  issues with double brackets and other mismatches between LaTeX and
  HTML outputs (see issue #244 reported by zhi-wang).

* The setup function now also returns the version of the extension (see
  issue #239 reported by lcnittl).

2.2.0 (5 March 2021)
--------------------

* Support the ``:any:`` role (see issue #232).

* New natbib/biblatex inspired roles for textual and parenthetical
  citation references (see issue #203 reported by matthew-brett).
  For textual citation references, use ``:cite:t:``
  and for parenthetical citation references, use ``:cite:p:``.
  The old ``:cite:`` role is an alias for ``:cite:p:``.

* Use the ``s`` suffix to include the full author list
  rather than abbreviating it with "et al.":
  ``:cite:ts:``, ``:cite:ps:``.

* For textual citation references,
  use the ``c`` prefix to capitalize the first letter:
  ``:cite:ct:``, ``:cite:cts:``.

* New natbib inspired roles for citing
  just the author, year, or label, optionally with brackets,
  and optionally capitalizing the first letter of the author:
  ``:cite:author:``, ``:cite:authorpar:``,
  ``:cite:cauthor:``, ``:cite:cauthorpar:``
  ``:cite:year:``, ``:cite:yearpar:``,
  ``:cite:label:``, ``:cite:labelpar:``
  (see issue #71 reported by bk322).

* To configure your referencing style,
  an optional config setting ``bibtex_reference_style`` has been added.
  If not specified, this defaults to the ``label`` style,
  which will use the label to format citation references, matching the
  referencing style as in previous versions.
  The other style currently available is ``author_year``, for author-year
  style referencing.

* Reference styles can be fully customized to your heart's desire
  (see issue #203 reported by amichuda).
  They are based on pybtex's template system, which was already used for
  customizing bibliography styles.
  Refer to the user documentation for examples, and to the API documentation
  for full details.

* Other packages can register custom reference styles through entry points.
  Refer to the user documentation for details.

* Propagate pybtex FieldIsMissing exception as a warning (see issue
  #235 reported by Zac-HD).

2.1.4 (8 January 2021)
----------------------

* Fix ValueError exception when having citations from orphans (see issue #228,
  reported by VincentRouvreau).

2.1.3 (1 January 2021)
----------------------

* Sphinx 2.1 or later is now formally required (up from 2.0).

* Fix unresolved references when running the latex build immediately after
  the html build, or when rerunning the html build after deleting the
  generated html files without deleting the pickled doctrees/environment
  (see issue #226, reported by skirpichev).

* No longer insert user defined header for bibliography directives if there are
  no citations in it.

* Warnings now consistently provide source file and line number of where the
  issue originated.

* Simpler and faster implementation of footcite and footbibliography.

* Improved type annotations throughout the API, now using forward
  declarations where possible.

2.1.2 (30 December 2020)
------------------------

* Fix KeyError exception when building documents with footbibliography
  directives but without any footnotes needing to be generated for this
  directive (see issue #223, reported by drammock).

2.1.1 (29 December 2020)
------------------------

* Fix latex builder KeyError exception (see issue #221, reported by jedbrown).

* Fix citation references across documents in latex build.

2.1.0 (28 December 2020)
------------------------

* The extension no longer relies on the ``bibtex.json`` method. Instead, the
  extension now postpones identifying all citation cross-references to
  Sphinx's consistency check phase.
  The actual citation references and bibliography citations
  are then generated in the resolve phase using post-transforms.
  As a result, ``bibtex.json`` is no longer needed and thus
  Sphinx no longer needs to run twice as in the past if the file did not exist
  (closes issues #214 and #215).
  *Thanks to everyone who chimed in on this, especially everyone who
  made helpful suggestions to find better implementation approaches,
  and everyone who helped with testing.*

* Citations with multiple keys will now reside in the same bracket
  (closes issue #94).

* Consistent use of doctutils note_explicit_target to set ids, to ensure no
  clashing ids.

* Improved and robustified test suite, using regular expressions to verify
  generated html.

* The test suite now includes a patched version of the awesome but abandoned
  sphinx-natbib extension, to help comparing and testing implementations and
  features.
  The long term intention is to fully support sphinx-natbib style citations.

* **BACKWARD INCOMPATIBLE**
  The API has been refactored to accommodate the new design.
  Refer to the API documentation for details.

2.0.0 (12 December 2020)
------------------------

* There is a new ``footcite`` role and a new ``footbibliography``
  directive, to allow easy and simple local (per document)
  bibliographies through footnotes.
  See issues #184 and #185.

* Parallel builds are now finally supported.
  See issues #80, #96, and #164, as well as pull request #210.

* **BACKWARD INCOMPATIBLE**
  To enable parallel builds, a new mandatory
  config setting ``bibtex_bibfiles`` has been added. This setting
  specifies all bib files used throughout the project,
  relative to the source folder.

* **BACKWARD INCOMPATIBLE**
  The encoding of bib files has been moved to an optional
  config setting ``bibtex_encoding``. The ``:encoding:``
  option is no longer supported.

* Headers for ``bibliography`` and ``footbibliography`` directives
  can be configured via the ``bibtex_bibliography_header`` and
  ``bibtex_footbibliography_header`` config setting.

* The ``bibliography`` directive no longer requires the bib files
  to be specified as an argument. However, if you do, citations will
  be constrained to those bib files.

* Support newlines/whitespace around cite keys when multiple keys are
  specified.
  Thanks to dizcza for help with testing.
  See issue #205 and pull request #206.

* Improve citation ordering code (reported by ukos-git, see issue
  #182).

* The unresolved citations across documents issue has been resolved.
  The extension stores all citation information in a ``bibtex.json`` file.
  If it does not exist, the file will be created on
  your first sphinx build, and you will have to rerun the build
  to make use of it. The file is automatically kept up to date,
  with a warning whenever you need to rerun the build.
  Thanks to dizcza for help with testing.
  See issues #197 and #204. Also see pull request #208.

* Migrate test suite to pytest, using sphinx's testing fixtures.

* **BACKWARD INCOMPATIBLE**
  The API has been refactored.
  Some functions have moved to different modules.
  Refer to the API documentation for details.

* Drop Python 3.5 support.

* Add Python 3.9 support.

1.0.0 (20 September 2019)
-------------------------

* Drop Python 2.7 and 3.4 support (as upstream sphinx has dropped
  support for these as well).

* Add Python 3.8 support (contributed by hroncok).

* Update for Sphinx 2.x, and drop Sphinx 1.x support (as there is too
  much difference between the two versions).

* Non-bibtex citations will now no longer issue warnings (fix
  contributed by chrisjsewell).

* Switch to codecov for coverage reporting.

0.4.2 (7 January 2018)
----------------------

* Drop Python 3.3 support, add Python 3.7 support.

* Work around issue with sphinx-testing on Fedora (reported by
  jamesjer in issue #157, fix contributed by mitya57 in pull request
  #158).

0.4.1 (28 November 2018)
------------------------

* Disable tinkerer test due to upstream bug.

* Remove crossref test due to changed upstream behaviour in pybtex.

* Fix latex test to match new upstream code generation.

* Fix documentation of encoding option (contributed by Kai Mühlbauer).

* Migrate to sphinx.util.logging in favour of old deprecated logging
  method.

0.4.0 (19 April 2018)
---------------------

* Remove latexcodec and curly bracket strip functionality, as this is
  now supported by pybtex natively (see issue #127, reported by
  erosennin).

* Fix tests failures with Sphinx 1.7 (see pull request #136, reported
  and fixed by mitya57).

0.3.6 (25 September 2017)
-------------------------

* Real fix for issue #111 (again reported by jamesjer).

* Fix test regressions due to latest Sphinx updates (see issues #115,
  #120, #121, and #122, reported by ndarmage and ghisvail).

* Fix test regressions on ascii locale (see issue #121, reported by
  ghisvail).

* Support and test Python 3.6.

0.3.5 (22 February 2017)
------------------------

* Fix extremely high memory usage when handling large bibliographies
  (reported by agjohnson, see issue #102).

* Fix tests for Sphinx 1.5.1 (see issue #111, reported by jamesjer).

0.3.4 (20 May 2016)
-------------------

* Document LaTeX workaround for ``:cite:`` in figure captions
  (contributed by xuhdev, see issue #92 and pull request #93).

* Add ``bibtex_default_style`` config value to override the default
  bibliography style (see issue #91 and pull request #97).

* Support Python 3.5 (see issue #100).

0.3.3 (23 October 2015)
-----------------------

* Add per-bibliography key prefixes, enabling local bibliographies to
  be used in isolation from each other (see issue #87, reported by
  marscher).

* Documentation now points to new location of pybtex on bitbucket.

* Simplified testing code by using the new sphinx_testing package.

0.3.2 (20 March 2015)
---------------------

* Document how to create custom label styles (see issue #77, reported
  by tino).

* Disable parallel_read_safe for Sphinx 1.3 and later (see issue #80,
  reported by andreacassioli).

0.3.1 (10 July 2014)
--------------------

* Fix for ``type_.lower()`` bug: pybtex 0.18 expects type to be a
  string (this fixes issue #68 reported by jluttine).

0.3.0 (4 May 2014)
------------------

* **BACKWARD INCOMPATIBLE**
  The alpha style is now default, so citations are labelled in a way
  that is more standard for Sphinx. To get the old behaviour back, add
  ``:style: plain`` to your bibliography directives.

* **BACKWARD INCOMPATIBLE**
  :meth:`~sphinxcontrib.bibtex.cache.Cache.is_cited` has been removed.
  Use :meth:`~sphinxcontrib.bibtex.cache.Cache.get_cited_docnames` instead,
  which will return an empty list for keys that are not cited.

* Improved support for local bibliographies (see issues #52, #62, and
  #63; test case provided by Boris Kheyfets):

  - New ``docname`` and ``docnames`` filter identifiers.

  - Filter expressions now also support set literals and the operators
    ``in``, ``not in``, ``&``, and ``|``.

  See documentation for details.

* Multiple comma-separated citation keys per cite command (see issue
  #61, suggested by Boris Kheyfets).

* Add support for pypy and Python 3.4.

* Drop support for Python 2.6 and Python 3.2.

* Drop 2to3 and instead use six to support both Python 2 and 3 from a
  single code base.

* Simplify instructions for custom styles.

* Various test suite improvements.

0.2.9 (9 October 2013)
----------------------

* Upgrade to the latest pybtex-docutils to produce more optimal html output
  (specifically: no more nested ``<span>``\ s).

* Remove latex codec code, and rely on latexcodec package instead.

* :class:`FilterVisitor` has been removed from the public API.
  Use :meth:`~sphinxcontrib.bibtex.cache.Cache.get_bibliography_entries`
  instead.

* Fix upstream Sphinx bug concerning LaTeX citation hyperlinks
  (contributed by erikb85; see pull request #45).

* Fix most pylint warnings, refactor code.

0.2.8 (7 August 2013)
---------------------

* Use pybtex-docutils to remove dependency on pybtex.backends.doctree.

0.2.7 (4 August 2013)
---------------------

* Integrate with coveralls.io, first release with 100% test coverage.

* Minor bug fixes and code improvements.

* Remove ordereddict dependency for Python 2.7 and higher (contributed
  by Paul Romano, see pull requests #27 and #28).

* New ``:filter:`` option for advanced filtering (contributed by
  d9pouces, see pull requests #30 and #31).

* Refactor documentation of advanced features.

* Document how to create custom pybtex styles (see issues #25, #29,
  and #34).

* Code is now mostly pep8 compliant.

0.2.6 (2 March 2013)
--------------------

* For unsorted styles, citation entries are now sorted in the order
  they are cited, instead of following the order in the bib file, to
  reflect more closely the way LaTeX handles unsorted styles
  (addresses issue #15).

* Skip citation label warnings on Sphinx [source] links (issue #17,
  contributed by Simon Clift).

0.2.5 (18 October 2012)
-----------------------

* Duplicate label detection (issue #14).

* New ``:labelprefix:`` option to avoid duplicate labels when having
  multiple bibliographies with a numeric label style (addresses
  issue #14).

0.2.4 (24 August 2012)
----------------------

* New options for the bibliography directive for rendering the
  bibliography as bullet lists or enumerated lists: ``:list:``,
  ``:enumtype:``, and ``:start:``.

* Minor latex codec fixes.

* Turn exception into warning when a citation cannot be relabeled
  (fixes issue #2).

* Document LaTeX encoding, and how to turn it off (issue #4).

* Use pybtex labels (fixes issue #6 and issue #7).

* Cache tracked citation keys and labels, and bibliography enumeration
  counts (fixes issues with citations in repeated Sphinx runs).

* Bibliography ids are now unique across documents (fixes issue that
  could cause the wrong bibliography to be inserted).

* The plain style is now the default (addresses issue #9).

0.2.3 (30 July 2012)
--------------------

* Document workaround for Tinkerer (issue #1).

* Use tox for testing.

* Full 2to3 compatibility.

* Document supported versions of Python (2.6, 2.7, 3.1, and 3.2).

0.2.2 (6 July 2012)
-------------------

* Documentation and manifest fixes.

0.2.1 (19 June 2012)
--------------------

* First public release.
