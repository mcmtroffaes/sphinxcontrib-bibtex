Referencing Styles
==================

Abstract Base Classes
---------------------

.. automodule:: sphinxcontrib.bibtex.style.referencing
   :members:

Basic Styles
------------

Basic styles that support both textual and parenthetical citations.
Should provide roles with names
``t``, ``p``, ``ct``, ``cp``, ``ts``, ``ps``, ``cts``, and ``pts``,
Here, ``t`` stands for textual and ``p`` for parenthetical.
The ``c`` prefix causes the first letter to be capitalized,
and the ``s`` suffix causes all authors to be named rather than
shortening the list using "et al." or some other suffix as
speficied by the style.

.. automodule:: sphinxcontrib.bibtex.style.referencing.basic_label
   :members:

.. automodule:: sphinxcontrib.bibtex.style.referencing.basic_author_year
   :members:

Extra Styles
------------

For styles providing additional roles, e.g. for citations that
specifically use the label, the author, the year, etc.
The convention for these styles is to have one role for producing
whichever text needs to be had, and to have "par" suffix
in the role name if the citation text needs to be embedded in
brackets (for example "label" and "labelpar").

.. automodule:: sphinxcontrib.bibtex.style.referencing.extra_label
   :members:

.. automodule:: sphinxcontrib.bibtex.style.referencing.extra_author
   :members:

.. automodule:: sphinxcontrib.bibtex.style.referencing.extra_year
   :members:

Full Styles
-----------

For styles that combine a basic style with one or more extra styles.

.. automodule:: sphinxcontrib.bibtex.style.referencing.label
   :members:

.. automodule:: sphinxcontrib.bibtex.style.referencing.author_year
   :members:
