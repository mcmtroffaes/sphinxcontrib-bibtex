Footbib Extension Usage
=======================

Roles and Directives
--------------------

.. rst:role:: footcite

   Create a footnote reference to a bibliographic entry. For example:

   .. code-block:: rest

      See :footcite:`1987:nelson` for an introduction to non-standard analysis.

   which would be equivalent to the following LaTeX code:

   .. code-block:: latex

      See \footcite{1987:nelson} for an introduction to non-standard analysis.

   Multiple comma-separated keys can be specified at once:

   .. code-block:: rest

      See :footcite:`1987:nelson,2001:schechter`.

.. rst:directive:: .. footbibliography:: refs.bib [...]

   Create footnotes for all references that are cited in the current
   document. For example:

   .. code-block:: rest

     .. footbibliography:: refs.bib

   which would be roughly equivalent to the following LaTeX code:

   .. code-block:: latex

      \footbibliography{refs.bib}

   You can also pick a bibliography style, using the ``style`` option.
   The ``alpha`` style is the default.
   Other supported styles are ``plain``, ``unsrt``, and ``unsrtalpha``.
   You can also create your own style (see :ref:`bibtex-custom-formatting`).

   .. code-block:: rest

     .. footbibliography:: refs.bib
        :style: unsrt

   You can also set the encoding of the bibliography files, using the
   ``encoding`` option.

   .. code-block:: rest

     .. footbibliography:: refs.bib
        :encoding: latin

   LaTeX control characters are automatically converted to unicode 
   characters (for instance, to convert ``\'e`` into ``é``). Be sure 
   to write ``\%`` when you intend to format a percent sign.
