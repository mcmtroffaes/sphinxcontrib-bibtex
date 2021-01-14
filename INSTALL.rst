Install the module with ``pip install sphinxcontrib-bibtex``, or from
source using ``python setup.py install``. Then add:

.. code-block:: python

   extensions = ['sphinxcontrib.bibtex']
   bibtex_bibfiles = ['refs.bib']

to your project's Sphinx configuration file ``conf.py``.

Minimal Example
---------------

In your project's documentation, you can use
``:cite:t:`` for textual citation references,
``:cite:p:`` for parenthetical citation references,
and ``.. bibliography::`` for inserting the bibliography.
For `example <https://github.com/mcmtroffaes/sphinxcontrib-bibtex/tree/develop/test/roots/test-debug_minimal_example>`_:

.. code-block:: rest

   See :cite:t:`1987:nelson` for an introduction to non-standard analysis.
   Non-standard analysis is fun :cite:p:`1987:nelson`.

   .. bibliography::

where :file:`refs.bib` would contain an entry::

   @Book{1987:nelson,
     author = {Edward Nelson},
     title = {Radically Elementary Probability Theory},
     publisher = {Princeton University Press},
     year = {1987}
   }

In the default style, this will get rendered as:

See Nelson [Nel87a]_ for an introduction to non-standard analysis.
Non-standard analysis is fun [Nel87a]_.

.. [Nel87a] Edward Nelson. *Radically Elementary Probability Theory*. Princeton University Press, 1987.

Citations in sphinx are resolved globally across all documents.
Typically, you have a single :rst:dir:`bibliography` directive across
your entire project which collects all citations.
Advanced use cases with multiple :rst:dir:`bibliography` directives
across your project are also supported, but some care
needs to be taken from your end to avoid duplicate citations.

In contrast, footnotes in sphinx are resolved locally per document.
To achieve local bibliographies per document, you can use citations
represented by footnotes as follows:

.. code-block:: rest

   Non-standard analysis is lovely. :footcite:`1987:nelson`

   .. footbibliography::

which will get rendered as:

Non-standard analysis is lovely. [#Nel87b]_

.. [#Nel87b] Edward Nelson. *Radically Elementary Probability Theory*. Princeton University Press, 1987.

Typically, you have a single :rst:dir:`footbibliography` directive
at the bottom of each document that has :rst:role:`footcite` citations.
Advanced use cases with multiple :rst:dir:`footbibliography` directives
per document are also supported. Since everything is local,
there is no concern with duplicate citations when using footnotes.
