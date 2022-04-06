"""Docstring for some_module. :cite:`testmodule`"""


def func(funcarg):
    """Docstring for function func.

    Long description goes here. See :cite:`testfunc`.

    :param funcarg: Docstring for parameter. :cite:`testfuncarg`
    """


a = 1
"""Docstring for variable a.

Long description goes here. See :cite:`testdata`.
"""


class Foo:
    """Docstring for class Foo.

    Long description goes here. See :cite:`testclass`.
    """

    b = 2
    """Docstring for class attribute b.

    Long description goes here. See :cite:`testclassattr`.
    """

    def __init__(self, initarg):
        """Docstring for constructor.

        Long description goes here. See :cite:`testinit`

        :param initarg: Docstring for parameter. :cite:`testinitarg`
        """

        self.c = 3
        """Docstring for instance attribute c.

        Long description goes here. See :cite:`testinstanceattr`.
        """

    def method(self, methodarg):
        """Docstring for method.

        Long description goes here. See :cite:`testmethod`.

        :param methodarg: Docstring for parameter. :cite:`testmethodarg`
        """
