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

.. rst:directive:: .. footbibliography::

   Create footnotes at this location for all references that are cited
   in the current document. You normally add this once at the very bottom
   of any document with footnote citations.

   If specified multiple times in the same document, footnotes are only
   created for references that do not yet have a footnote earlier in the
   document.

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

Custom Footnote Paragraph Header
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, the ``.. footbibliography::`` simply inserts a paragraph.
The ``bibtex_footbibliography_header`` configuration value can be set
to add a header to this. For example, in your ``conf.py`` you could
have:

.. code-block:: python

   bibtex_footbibliography_header = ".. rubric:: Citations"

will ensure that every paragraph of footnote citations will have a
rubric.
