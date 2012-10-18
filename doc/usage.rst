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

   which would be roughly equivalent to the following LaTeX code:

   .. code-block:: latex

      \begin{thebibliography}{1}
        \bibitem{1987:nelson}
        Edward~Nelson
        \newblock {\em Radically Elementary Probability Theory}.
        \newblock Princeton University Press, 1987.
      \end{thebibliography}

   Note that, unlike LaTeX, the :rst:dir:`bibliography` directive does
   not generate a default section title.

   .. warning::

      Sphinx may not be able to create an entry for :rst:role:`cite` keys
      when your :rst:dir:`bibliography` directive
      resides in a different document;
      see :ref:`issue-unresolved-citations`
      for more information and workarounds.

   You can also pick a bibliography style, using the ``style`` option.
   This is not yet quite as useful, as only ``plain`` and ``unsrt``
   are supported.
   The ``plain`` style is the default.

   .. code-block:: rest

     .. bibliography:: refs.bib
        :style: unsrt

   All citations have numbered labels, as in the ``plain`` LaTeX
   bibliography style, regardless of the style chosen. This limitation
   might be lifted in a future version.

   If you have multiple bibliographies, and experience duplicate labels,
   use the ``labelprefix`` option.

   .. code-block:: rest

     .. rubric:: References

     .. bibliography:: refs.bib
        :cited:
        :labelprefix: A

     .. rubric:: Further reading

     .. bibliography:: refs.bib
        :notcited:
        :labelprefix: B

   .. warning::

      Sphinx will attempt to resolve references to the bibliography
      across all documents, so you must take care that no citation key
      is included more than once.

   You can also set the encoding of the bibliography files, using the
   ``encoding`` option.

   .. code-block:: rest

     .. bibliography:: refs.bib
        :encoding: latex+latin

   Note that, usually, you want to prepend your encoding with
   ``latex+``, in order to convert LaTeX control characters to unicode
   characters (for instance, to convert ``\'e`` into ``é``). The latex
   codec is invoked by default, for your convenience. Be sure to write
   ``\%`` when you intend to format a percent sign.

   You can also change the type of list used for rendering the
   bibliography. By default, a paragraph of standard citations is
   generated. However, instead, you can also generate a bullet list,
   or an enumerated list.

   .. code-block:: rest

     .. bibliography:: refs1.bib
        :list: bullet
        :all:

     .. bibliography:: refs2.bib
        :list: enumerated
        :all:

   Note that citations to these types of bibliography lists will not
   be resolved.

   For enumerated lists, you can also specify the type (default is
   ``arabic``), and the start of the sequence (default is ``1``).

   .. code-block:: rest

     .. bibliography:: refs2.bib
        :list: enumerated
        :enumtype: upperroman
        :start: 3
        :all:

   The enumtype can be any of
   ``arabic`` (1, 2, 3, ...),
   ``loweralpha`` (a, b, c, ...),
   ``upperalpha`` (A, B, C, ...),
   ``lowerroman`` (i, ii, iii, ...), or
   ``upperroman`` (I, II, III, ...).

   The start can be any positive integer (1, 2, 3, ...) or
   ``continue`` if you wish the enumeration to continue from the last
   :rst:dir:`bibliography` directive.
   This is helpful if you split up your bibliography but
   still want to enumerate the entries continuously.

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

Encoding: Percent Signs
~~~~~~~~~~~~~~~~~~~~~~~

When using the LaTeX codec (which is by default), be sure to write
``\%`` for percent signs at all times (unless your file contains a
genuine comment), otherwise the bibtex lexer will ignore the remainder
of the line.

If you don't want any LaTeX symbols to be reinterpreted as unicode,
use the option ``:encoding: utf`` (without the ``latex+`` prefix).

.. _issue-unresolved-citations:

Unresolved Citations Across Documents
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you cite something that has its bibliography in another document,
then, at the moment, the extension may, or may not, realise that it
has to add this citation.
There are a few ways to work around this problem:

* Use the option ``:all:`` in the :rst:dir:`bibliography`
  directive (which will simply cause all entries to be included).

* Ensure that the :rst:dir:`bibliography` directive is processed after
  all :rst:role:`cite`\ s. Sphinx appears to process files in an
  alphabetical manner. For instance, in case you have only one file
  containing a :rst:dir:`bibliography` directive, simply name that
  file :file:`zreferences.rst`.

Hopefully, this limitation can be lifted in a future release.

KeyError When Using ``:style: plain``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When using the ``plain`` style, or any style that sorts entries, pybtex
may raise ``KeyError: 'author'`` for entries that have no author. A
patch has been submitted upstream:

https://code.launchpad.net/~matthias-troffaes/pybtex/sorting-bugfix

Duplicate Labels When Using ``:style: plain``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

With ``:style: plain``, label are numerical,
restarting at ``[1]`` for each :rst:dir:`bibliography` directive.
Consequently, when inserting multiple :rst:dir:`bibliography` directives
with ``:style: plain``,
you are bound to get duplicate labels for entries.
There are a few ways to work around this problem:

* Use a single bibliography directive for all your references.

* Use the ``labelprefix`` option, as documented above.

* Use a style that has non-numerical labelling.
  Unfortunately, pybtex does not yet support such styles.
  A patch for non-numerical styles, such as ``:style: alpha``,
  has been submitted upstream:

  https://code.launchpad.net/~matthias-troffaes/pybtex/label-alpha

  When this becomes part of pybtex,
  the plan is to change the default citation style to ``:style: alpha``,
  as this style is also more in line with
  how citations are usually labelled in Sphinx.
