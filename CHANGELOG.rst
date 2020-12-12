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
  multiple bibliographies with a numerical label style (addresses
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
