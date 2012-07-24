Usage
=====

Roles and Directives
--------------------

.. rst:role:: cite

   Create a citation to a bibliographic entry. For example:

   .. code-block:: rest

      See :cite:`1987:nelson` for an introduction to non-standard analysis.

   which would be equivalent to the following LaTeX code:

   .. code-block:: latex

      See \cite{1987:nelson} for an introduction to non-standard analysis.

.. rst:directive:: .. bibliography:: refs.bib [...]

   Create bibliography for all cited references. The ``all`` flag
   forces all references to be included (equivalent to ``\nocite{*}``
   in LaTeX). The ``notcited`` flag causes all references that were
   not cited to be included. The ``cited`` flag is recognized as well
   but is entirely optional. For example:

   .. code-block:: rest

     .. rubric:: References

     .. bibliography:: refs.bib
        :cited:

     .. rubric:: Further reading

     .. bibliography:: refs.bib
        :notcited:

   .. warning::

      Sphinx will attempt to resolve references to the bibliography
      across all documents, so you must take care that no citation key
      is included more than once.

   You can also pick a bibliography style, using the ``style`` option.
   This is not yet quite as useful, as only ``unsrt`` is supported,
   which is also the default.

   .. code-block:: rest

     .. bibliography:: refs.bib
        :style: unsrt

   All citations have numbered labels, as in the ``plain`` LaTeX
   bibliography style, regardless of the style chosen. This limitation
   might be lifted in a future version.

   You can also set the encoding of the bibliography files, using the
   ``encoding`` option.

   .. code-block:: rest

     .. bibliography:: refs.bib
        :encoding: latin

.. XXX not documenting disable-curly-bracket-strip for now; might remove it

   Finally, curly brackets are automatically removed when the bib file
   is parsed. Usually, this is what you want. If you desire to disable
   this behaviour, use the ``disable-curly-bracket-strip`` option:

   .. code-block:: rest

     .. bibliography:: refs.bib
        :disable-curly-bracket-strip:

Known Issues and Workarounds
----------------------------

Tinkerer
~~~~~~~~

To use the bibtex extension with `Tinkerer <http://www.tinkerer.me/>`_,
be sure to specify the bibtex extension first in your ``conf.py`` file::

    extensions = ['sphinxcontrib.bibtex', 'tinkerer.ext.blog', 'tinkerer.ext.disqus']
