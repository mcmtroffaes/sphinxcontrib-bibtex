Bibtex Extension Usage
======================

The extension stores all citation information in a ``bibtex.json`` file
in the source folder.
If it does not exist, the file will be created on
your first sphinx build, and you will have to rerun the build
to make use of it. The file is automatically kept up to date,
with a warning whenever you need to rerun the build
(i.e. whenever your citations change).
The file can be stored in version control
if you do not want your users to have to run sphinx twice.

Configuration
-------------

To configure the extension, in your ``conf.py`` file,
set ``bibtex_bibfiles`` to your list of bib files.
For instance, a minimal configuration may look as follows:

.. code-block:: rest

   extensions = ['sphinxcontrib.bibtex']
   bibtex_bibfiles = ['refs.bib']

Roles and Directives
--------------------

.. rst:role:: cite

   Create a citation to a bibliographic entry. For example:

   .. code-block:: rest

      See :cite:`1987:nelson` for an introduction to non-standard analysis.

   which would be equivalent to the following LaTeX code:

   .. code-block:: latex

      See \cite{1987:nelson} for an introduction to non-standard analysis.

   Multiple comma-separated keys can be specified at once:

   .. code-block:: rest

      See :cite:`1987:nelson,2001:schechter`.

.. rst:directive:: .. bibliography::

   Create bibliography for all cited references. The ``all`` flag
   forces all references to be included (equivalent to ``\nocite{*}``
   in LaTeX). The ``notcited`` flag causes all references that were
   not cited to be included. The ``cited`` flag is recognized as well
   but is entirely optional. For example:

   .. code-block:: rest

     .. bibliography::
        :cited:

   which would be roughly equivalent to the following LaTeX code:

   .. code-block:: latex

      \begin{thebibliography}{1}
        \bibitem{1987:nelson}
        Edward~Nelson
        \newblock {\em Radically Elementary Probability Theory}.
        \newblock Princeton University Press, 1987.
      \end{thebibliography}

   You can also pick a bibliography style, using the ``style`` option.
   The ``alpha`` style is the default.
   Other supported styles are ``plain``, ``unsrt``, and ``unsrtalpha``.
   You can also create your own style (see :ref:`bibtex-custom-formatting`).

   .. code-block:: rest

     .. bibliography:: refs.bib
        :style: unsrt

   .. warning::

      Sphinx will attempt to resolve references to the bibliography
      across all documents, so you must take care that no citation key
      is included more than once.

   You can also set the encoding of the bibliography files, using the
   ``encoding`` option.

   .. code-block:: rest

     .. bibliography:: refs.bib
        :encoding: latin

   LaTeX control characters are automatically converted to unicode 
   characters (for instance, to convert ``\'e`` into ``é``). Be sure 
   to write ``\%`` when you intend to format a percent sign.

.. XXX not documenting disable-curly-bracket-strip for now; might remove it

   Finally, curly brackets are automatically removed when the bib file
   is parsed. Usually, this is what you want. If you desire to disable
   this behaviour, use the ``disable-curly-bracket-strip`` option:

   .. code-block:: rest

     .. bibliography:: refs.bib
        :disable-curly-bracket-strip:

Advanced Features
-----------------

Bullet Lists and Enumerated Lists
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 0.2.4

You can change the type of list used for rendering the
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

Label Prefixing
~~~~~~~~~~~~~~~

.. versionadded:: 0.2.5

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

.. _section-key-prefixing:

Key Prefixing
~~~~~~~~~~~~~

.. versionadded:: 0.3.3

If you have multiple bibliographies, and you would like entries to be
repeated in different documents, then use the ``keyprefix`` option.

For example, suppose you have two documents, and you would like to cite
``boole1854`` in both of these doucments, with the bibliography entries
showing in both of the documents. In one document you could have:

.. code-block:: rest

   See :cite:`a-boole1854`

   .. bibliography:: refs.bib
      :labelprefix: A
      :keyprefix: a-

whilst in the other document you could have:

.. code-block:: rest

   See :cite:`b-boole1854`

   .. bibliography:: refs.bib
      :labelprefix: B
      :keyprefix: b-

The bibliographies will then both generate an entry for ``boole1854``,
with links and backlinks as expected.

.. seealso::

   :ref:`section-local-bibliographies`

Filtering
~~~~~~~~~

.. versionadded:: 0.2.7

Whilst the ``cited``, ``all``, and ``notcited`` options
will cover many use cases,
sometimes more advanced selection of bibliographic entries is desired.
For this purpose, you can use the ``filter`` option:

.. code-block:: rest

   .. bibliography:: refs.bib
      :list: bullet
      :filter: author % "Einstein"

The string specified in the filter option must be a valid Python
expression.

.. note::

   The expression is parsed using :func:`ast.parse`
   and then evaluated using an :class:`ast.NodeVisitor`,
   so it should be reasonably safe against malicious code.

The filter expression supports:

* The boolean operators ``and``, ``or``.

* The unary operator ``not``.

* The comparison operators ``==``, ``<=``, ``<``, ``>=``, and ``>``.

* Regular expression matching using the ``%`` operator, where the left
  hand side is the string to be matched, and the right hand side is
  the regular expression. Matching is case insensitive. For example:

    .. code-block:: rest

       .. bibliography:: refs.bib
          :list: bullet
          :filter: title % "relativity"

  would include all entries that have the word "relativity" in the title.

  .. note::

     The implementation uses :func:`re.search`.

* Single and double quoted strings, such as ``'hello'`` or ``"world"``.

* Set literals, such has ``{"hello", "world"}``, as well as
  the set operators ``&``, ``|``, ``in``, and ``not in``.

  .. versionadded:: 0.3.0

* Various identifiers, such as:

  - ``type`` is the entry type, as a lower case string
    (i.e. ``"inproceedings"``).

  - ``key`` is the entry key, as a lower case string
    (this is because keys are considered case insensitive).

  - ``cited`` evaluates to ``True`` if the entry was cited in the document,
    and to ``False`` otherwise.

  - ``docname`` evaluates to the name of the current document.

    .. versionadded:: 0.3.0

  - ``docnames`` evaluates to a set of names from which the entry is cited.

    .. versionadded:: 0.3.0

  - ``True`` and ``False``.

  - ``author`` is the entry string of authors
    in standard format (last, first), separated by "and".

  - ``editor`` is similar to ``author`` but for editors.

  - Any other (lower case) identifier evaluates to a string
    containing the value of
    the correspondingly named field, such as
    ``title``, ``publisher``, ``year``, and so on.
    If the item is missing in the entry
    then it evaluates to the empty string.
    Here is an example of how one would typically write an expression
    to filter on an optional field:

    .. code-block:: rest

       .. bibliography:: refs.bib
          :list: bullet
          :filter: cited and year and (year <= "2003")

    which would include all cited entries that have a year
    that is less or equal than 2003; any entries that do not
    specify a year would be omitted.

.. _section-local-bibliographies:

Local Bibliographies
~~~~~~~~~~~~~~~~~~~~

Both the ``keyprefix`` and ``filter`` options can be used
to achieve local bibliographies.

The ``filter`` system for local bibliographies is the simplest one to
use, but offers the least amount of flexibility.  In particular, it
can only be used if no citation key is used in more than one
document. This is not always satisfied. If you need to cite the same
reference in multiple documents with references to multiple local
bibliographies, use the ``keyprefix`` system; see
:ref:`section-key-prefixing`.

To create a bibliography that includes only citations that were cited
in the current document, use the following filter:

.. code-block:: rest
                
   .. bibliography:: refs.bib
      :filter: docname in docnames

More generally, you can create bibliographies for
citations that were cited from specific documents only:

.. code-block:: rest

   .. bibliography:: refs.bib
      :filter: {"doc1", "doc2"} & docnames

This bibliography will include all citations that were cited from
:file:`doc1.rst` or :file:`doc2.rst`. Another hypothetical example:

.. code-block:: rest

   .. bibliography:: refs.bib
      :filter: cited and ({"doc1", "doc2"} >= docnames)

This bibliography will include all citations that were cited
in :file:`doc1.rst` or :file:`doc2.rst`, but nowhere else.

.. _bibtex-custom-formatting:

Custom Formatting, Sorting, and Labelling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:mod:`pybtex` provides a very powerful way to create and register new
styles, using setuptools entry points,
as documented here: http://docs.pybtex.org/api/plugins.html

Simply add the following code to your ``conf.py``:

.. code-block:: python

  from pybtex.style.formatting.unsrt import Style as UnsrtStyle
  from pybtex.style.template import toplevel # ... and anything else needed
  from pybtex.plugin import register_plugin

  class MyStyle(UnsrtStyle):

      def format_XXX(self, e):
          template = toplevel [
              # etc.
          ]
          return template.format_data(e)

  register_plugin('pybtex.style.formatting', 'mystyle', MyStyle)

Now ``mystyle`` will be available to you as a formatting style:

.. code-block:: rest

   .. bibliography:: refs.bib
      :style: mystyle

An minimal example is available here:
https://github.com/mcmtroffaes/sphinxcontrib-bibtex/tree/develop/test/custom_style

The formatting code uses a very intuitive template engine.
The source code for ``unsrt`` provides many great examples:
https://bitbucket.org/pybtex-devs/pybtex/src/master/pybtex/style/formatting/unsrt.py?at=master&fileviewer=file-view-default

The above example only demonstrates a custom formatting style plugin.
It is also possible to register custom author/editor naming plugins
(using the ``pybtex.style.names`` group)
labelling plugins
(using the ``pybtex.style.labels`` group),
and sorting plugins
(using the ``pybtex.style.sorting`` group).
A few minimal examples demonstrating how to create a custom label styles
are available here:

* https://github.com/mcmtroffaes/sphinxcontrib-bibtex/tree/develop/test/issue77
* https://github.com/mcmtroffaes/sphinxcontrib-bibtex/tree/develop/test/custom_labels

Known Issues and Workarounds
----------------------------

No Parallel Builds
~~~~~~~~~~~~~~~~~~

Because the extension needs to process documents in sequential order
to know what citation entries are cited, in the current design,
parallel builds are not supported. If parallel builds are important
for you, you can use the experimental :rst:role:`footcite` role
and :rst:dir:`footbibliography` directive
currently residing in the bibtex2 extension.
These convert citations into footnotes,
which are local to each document, and which therefore
do not have this limitation.

Encoding: Percent Signs
~~~~~~~~~~~~~~~~~~~~~~~

When using the LaTeX codec (which is by default), be sure to write
``\%`` for percent signs at all times (unless your file contains a
genuine comment), otherwise the bibtex lexer will ignore the remainder
of the line.

If you don't want any LaTeX symbols to be reinterpreted as unicode,
use the option ``:encoding: utf`` (without the ``latex+`` prefix).

Duplicate Labels When Using ``:style: plain``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

With ``:style: plain``, labels are numerical,
restarting at ``[1]`` for each :rst:dir:`bibliography` directive.
Consequently, when inserting multiple :rst:dir:`bibliography` directives
with ``:style: plain``,
you are bound to get duplicate labels for entries.
There are a few ways to work around this problem:

* Use a single bibliography directive for all your references.

* Use the ``labelprefix`` option, as documented above.

* Use a style that has non-numerical labelling,
  such as ``:style: alpha``.

LaTeX Backend Fails with Citations In Figure Captions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sphinx generates ``\phantomsection`` commands for references,
however LaTeX does not support these in figure captions.
You can work around this problem by adding the following code to
your ``conf.py``:

.. code-block:: python

   latex_elements = {
    'preamble': r'''
        % make phantomsection empty inside figures
        \usepackage{etoolbox}
        \AtBeginEnvironment{figure}{\renewcommand{\phantomsection}{}}
    '''
   }

Mismatch Between Output of HTML and LaTeX Backends
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sphinx's LaTeX writer currently collects all citations together,
and puts them on a separate page, with a separate title,
whereas the html writer puts citations
at the location where they are defined.
This issue will occur also if you use regular citations in Sphinx:
it has nothing to do with sphinxcontrib-bibtex per se.

To get a closer match between the two outputs,
you can tell Sphinx to generate a rubric title only for html:

.. code-block:: rest

   .. only:: html

      .. rubric:: References

   .. bibliography:: refs.bib

This code could be placed in your :file:`zreferences.rst`.

Alternatively, to remove the bibliography section title from the
LaTeX output, you can add the following to your LaTeX preamble:

.. code-block:: latex

   \usepackage{etoolbox}
   \patchcmd{\thebibliography}{\section*{\refname}}{}{}{}

