import pytest
from sphinx.testing.path import path


pytest_plugins = 'sphinx.testing.fixtures'
collect_ignore = ['roots']


@pytest.fixture(scope='session')
def rootdir() -> path:
    return path(__file__).parent.abspath() / 'roots'


# monkey patch for path class on old sphinx versions
if not hasattr(path, "read_text"):
    path.read_text = path.text  # type: ignore
