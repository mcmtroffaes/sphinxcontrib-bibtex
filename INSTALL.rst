Install the module with ``pip install sphinxcontrib-bibtex``, or from
source using ``python setup.py install``. Then add:

.. code-block:: python

   extensions = ['sphinxcontrib.bibtex']
   bibtex_bibfiles = ['refs.bib']

to your project's Sphinx configuration file ``conf.py``.

Minimal Example
---------------

In your project's documentation, you can then write for instance:

.. code-block:: rest

   See :cite:`1987:nelson` for an introduction to non-standard analysis.

   .. bibliography::

where refs.bib would contain an entry::

   @Book{1987:nelson,
     author = {Edward Nelson},
     title = {Radically Elementary Probability Theory},
     publisher = {Princeton University Press},
     year = {1987}
   }

In the default style, this will get rendered as:

See [Nel87a]_ for an introduction to non-standard analysis.

.. [Nel87a] Edward Nelson. *Radically Elementary Probability Theory*. Princeton University Press, 1987.

Similarly, with bibtex2:

.. code-block:: rest

   Non-standard analysis is lovely. :footcite:`1987:nelson`

which will get rendered as:

Non-standard analysis is lovely. [#Nel87b]_

.. [#Nel87b] Edward Nelson. *Radically Elementary Probability Theory*. Princeton University Press, 1987.
