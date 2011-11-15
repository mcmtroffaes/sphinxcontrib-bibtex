Testing the bibliography directive
==================================

Text
----

Huyghens :cite:`1657:huygens` wrote one of the first books on
probability theory.

Something that's not in the bib files is displayed as :cite:`no:such:key`.

Mix with a footnote [#note]_ and a regular citation [Test01]_.

Another citation :cite:`dreze:2000`.

Another reference to footnotes [#note]_ and [#note2]_.
More regular citations [Test01]_ and [Test02]_.

References
----------

.. bibliography:: test.bib unknown.bib subfolder/test.bib

.. bibliography:: unknown2.bib

Notes
-----

.. [#note] A footnote.
.. [#note2] Another footnote.

Regular Citations
-----------------

.. [Test01] A regular citation.
.. [Test02] Another regular citation.
