import pytest
from sphinx.testing.path import path


pytest_plugins = 'sphinx.testing.fixtures'
collect_ignore = ['roots']


@pytest.fixture(scope='session')
def rootdir():
    return path(__file__).parent.abspath() / 'roots'
