Footbib Extension Usage
=======================

Configuration
-------------

* ``footbib_bibfiles``: a list of bib files, must be set

* ``footbib_encoding``: encoding of the bib files (default:
  "utf-8-sig")

* ``footbib_default_style``: the default pybtex citation style
  (default: "alpha")

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

Advanced Features
-----------------

Multiple Footnote Paragraphs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rst:directive:: .. footbibliography::

   Create footnotes at this location for all references that are cited
   in the current document, but that have not been cited yet earlier
   in the document.

   This can be useful if you want to have multiple footnote paragraphs
   in the same document, rather than just a single paragraph with
   footnotes at the bottom of the document.
   
   You can also pick a bibliography style, using the ``style`` option.
   The ``alpha`` style is the default.
   Other supported styles are ``plain``, ``unsrt``, and ``unsrtalpha``.
   You can also create your own style (see :ref:`bibtex-custom-formatting`).

   .. code-block:: rest

     .. footbibliography::
        :style: unsrt
