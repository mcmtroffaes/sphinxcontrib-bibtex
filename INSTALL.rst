Install the module with ``pip install sphinxcontrib-bibtex``, or from
source using ``python setup.py install``. Then add:

.. code-block:: python

   extensions = ['sphinxcontrib.bibtex']

to your project's Sphinx configuration file ``conf.py``.

Minimal Example
---------------

In your project's documentation, you can then write for instance:

.. code-block:: rest

   See :cite:`1987:nelson` for an introduction to non-standard analysis.

   .. bibliography:: refs.bib

where refs.bib would contain an entry::

   @Book{1987:nelson,
     author = {Edward Nelson},
     title = {Radically Elementary Probability Theory},
     publisher = {Princeton University Press},
     year = {1987}
   }

In the default style, this will get rendered as:

See [Nel87]_ for an introduction to non-standard analysis.

.. [Nel87] Edward Nelson. *Radically Elementary Probability Theory*. Princeton University Press, 1987.
