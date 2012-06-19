The sphinxcontrib-bibtex extension allows bibtex references to be inserted into your documentation.

:author: Matthias C. M. Troffaes <matthias.troffaes@gmail.com>
:license: BSD, see LICENSE for details

Inspired by ``bibstuff.sphinxext.bibref`` by Matthew Brett.

The extension adds a :rst:dir:`bibliography` directive, and a
:rst:role:`cite` role, which work similarly to LaTeX's
``\bibliography`` and ``\cite`` commands.

Install the module using ``python setup.py install``, and add::

   extensions = ['sphinxcontrib.bibtex']

to your project's Sphinx configuration file ``conf.py``. In your
documentation, you can then write for instance:

.. code-block:: rest

   See :cite:`1987:nelson` for an introduction to non-standard analysis.

   .. bibliography:: refs.bib

where refs.bib would contain an entry::

   @Book{1987:nelson,
     author = {Edward Nelson},
     title = {Radically Elementary Probability Theory},
     publisher = {Princeton University Press},
     year = {1977},
     series = {Annals of Mathematical Studies}
   }
