Testing the fnbibliography directive
====================================

Text
----

Huyghens :fncite:`1657:huygens` wrote one of the first books on
probability theory.

Mix with a footnote [#note]_.

Another few citations: :fncite:`rockafellar:1970,1972:savage`.

Cite it twice: :fncite:`1657:huygens`.

Bad citation: :fncite:`keydoesnotexist`.

.. rubric:: Footnotes

.. [#note] A footnote.

.. rubric:: References

.. fnbibliography:: test.bib test2.bib subfolder/test.bib
