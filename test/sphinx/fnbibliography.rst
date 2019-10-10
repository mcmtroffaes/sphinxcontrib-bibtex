Testing the footbibliography directive
======================================

Text
----

Huyghens :footcite:`1657:huygens` wrote one of the first books on
probability theory.

Mix with a footnote [#note]_.

Another few citations: :footcite:`rockafellar:1970,1972:savage`.

Cite it twice: :footcite:`1657:huygens`.

Bad citation: :footcite:`keydoesnotexist`.

.. rubric:: Footnotes

.. [#note] A footnote.

.. rubric:: References

.. footbibliography:: test.bib test2.bib subfolder/test.bib
