"""Docstring for some_module. :cite:`testmodule`"""


def func(funcarg):
    """Docstring for function func. :cite:`testfunc`

    :param funcarg: Docstring for parameter. :cite:`testfuncarg`
    """


a = 1
"""Docstring for variable a. :cite:`testdata`"""


class Foo:
    """Docstring for class Foo. :cite:`testclass`"""

    b = 2
    """Docstring for class attribute b. :cite:`testclassattr`"""

    def __init__(self, initarg):
        """Docstring for constructor. :cite:`testinit`

        :param initarg: Docstring for parameter. :cite:`testinitarg`
        """

        self.c = 3
        """Docstring for instance attribute c. :cite:`testinstanceattr`"""

    def method(self, methodarg):
        """Docstring for method. :cite:`testmethod`

        :param methodarg: Docstring for parameter. :cite:`testmethodarg`
        """
