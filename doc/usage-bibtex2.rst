Bibtex2 Extension Usage
=======================

The bibtex2 extension is currently in an experimental state.
You can use it but things might still break in future releases.
The extension aims to be fully parallel safe, and aims to address
the long standing issue of unresolved citations across documents.
This needs a more drastic redesign, whence why it is developed
as a separate extension.

Configuration
-------------

* ``bibtex_bibfiles``: a list of bib files, must be set

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

Bib File Encoding
~~~~~~~~~~~~~~~~~

Set the ``bibtex_encoding`` configuration value to change the bib file
encoding. The default encoding is ``utf-8-sig``.

Custom Formatting
~~~~~~~~~~~~~~~~~

Set the ``bibtex_style`` configuration value to control the pybtex
formatting style. The default is ``alpha``. Other supported styles are
``plain``, ``unsrt``, and ``unsrtalpha``. You can also create your own
style (see :ref:`bibtex-custom-formatting`).

Multiple Footnote Paragraphs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sometimes you may want to have multiple footnote paragraphs in the
same document, rather than just a single paragraph with footnotes at
the bottom of the document. For this purpose, you can use the
following directive:

.. rst:directive:: .. footbibliography::

   Create footnotes at this location for all references that are cited
   in the current document, but that have no corresponding footnotes
   yet earlier in the document.

Custom Footnote Paragraph Footer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, every document containing a ``:footcite:`` gets a
``.. footbibliography::`` directive inserted at the end. The
``bibtex_footbib_footer`` configuration value can be set to change
this. For example, in your ``conf.py`` you could have:

.. code-block:: python

   bibtex_footbib_footer = """
   .. rubric:: Citations

   .. footbibliography::
   """

will ensure that every document containing footnote citations will
have a rubric for these citations.
