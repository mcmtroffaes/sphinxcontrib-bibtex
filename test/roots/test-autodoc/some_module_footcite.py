"""Docstring for some_module. :footcite:`testmodule`"""


def func(funcarg):
    """Docstring for function func. :footcite:`testfunc`

    :param funcarg: Docstring for parameter. :footcite:`testfuncarg`
    """


a = 1
"""Docstring for variable a. :footcite:`testdata`"""


class Foo:
    """Docstring for class Foo. :footcite:`testclass`"""

    b = 2
    """Docstring for class attribute b. :footcite:`testclassattr`"""

    def __init__(self, initarg):
        """Docstring for constructor. :footcite:`testinit`

        :param initarg: Docstring for parameter. :footcite:`testinitarg`
        """

        self.c = 3
        """Docstring for instance attribute c. :footcite:`testinstanceattr`"""

    def method(self, methodarg):
        """Docstring for method. :footcite:`testmethod`

        :param methodarg: Docstring for parameter. :footcite:`testmethodarg`
        """
