Installation
------------

Install the module with ``pip install sphinxcontrib-bibtex``, or from
source using ``pip install -e .``. Then add:

.. code-block:: python

   extensions = ['sphinxcontrib.bibtex']
   bibtex_bibfiles = ['refs.bib']

to your project's Sphinx configuration file ``conf.py``.

Installation with ``python setup.py install`` is discouraged due to potential
issues with the sphinxcontrib namespace.
