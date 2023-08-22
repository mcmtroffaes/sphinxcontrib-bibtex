import pytest
import sphinx

if sphinx.version_info < (7, 2):
    from sphinx.testing.path import path as Path
    _rootdir = Path(__file__).parent.abspath() / 'roots'
else:
    from pathlib import Path
    _rootdir = Path(__file__).parent.resolve() / 'roots'

pytest_plugins = 'sphinx.testing.fixtures'
collect_ignore = ['roots']


@pytest.fixture(scope='session')
def rootdir() -> Path:
    return _rootdir
