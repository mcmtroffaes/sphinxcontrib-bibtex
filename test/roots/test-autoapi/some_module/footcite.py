"""Docstring for some_module. :footcite:`testmodule`

.. footbibliography::
"""


def func(funcarg):
    """Docstring for function func.

    Long description goes here. See :footcite:`testfunc`.

    :param funcarg: Docstring for parameter. :footcite:`testfuncarg`

    .. footbibliography::
    """


a = 1
"""Docstring for variable a.

Long description goes here. See :footcite:`testdata`.

.. footbibliography::
"""


class Foo:
    """Docstring for class Foo.

    Long description goes here. See :footcite:`testclass`.

    .. footbibliography::
    """

    b = 2
    """Docstring for class attribute b.

    Long description goes here. See :footcite:`testclassattr`.

    .. footbibliography::
    """

    def __init__(self, initarg):
        """Docstring for constructor.

        Long description goes here. See :footcite:`testinit`.

        :param initarg: Docstring for parameter. :footcite:`testinitarg`

        .. footbibliography::
        """

        self.c = 3
        """Docstring for instance attribute c.

        Long description goes here. See :footcite:`testinstanceattr`

        .. footbibliography::
        """

    def method(self, methodarg):
        """Docstring for method.

        Long description goes here. See  :footcite:`testmethod`.

        :param methodarg: Docstring for parameter. :footcite:`testmethodarg`

        .. footbibliography::
        """
