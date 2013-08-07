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
