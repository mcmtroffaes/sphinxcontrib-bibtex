Testing the bibliography directive
==================================

Text
----

Huyghens :cite:`1657:huygens` wrote one of the first books on
probability theory.

Mix with a footnote [#note]_ and a regular citation [Test01]_.

Another citation :cite:`dreze:2000`.

Another reference to footnotes [#note]_ and [#note2]_.
More regular citations [Test01]_ and [Test02]_.

Extra reference to a footnote [#footnote-walley2004]_.

Extra reference to a citation [Wa04]_.

Another few citations: :cite:`rockafellar:1970,1972:savage`.

More citations: 

.. rubric:: References

.. bibliography:: test.bib subfolder/test.bib
   :all:
   :labelprefix: A

.. rubric:: References (Cited Test)

.. bibliography:: test2.bib
   :cited:
   :labelprefix: B

.. rubric:: References (Not Cited Test)

.. bibliography:: test2.bib
   :notcited:
   :labelprefix: C

.. rubric:: Footnotes

.. [#note] A footnote.
.. [#note2] Another footnote.
.. [#footnote-walley2004]

    Peter Walley, Renato Pelessoni, and Paolo Vicig. Journal of
    Statistical Planning and Inference, 126(1):119-151, November 2004.

.. rubric:: Citations

.. [Test01] A regular citation.
.. [Test02] Another regular citation.
.. [Wa04]

    Peter Walley, Renato Pelessoni, and Paolo Vicig. Journal of
    Statistical Planning and Inference, 126(1):119-151, November 2004.
