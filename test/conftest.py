from pathlib import Path

import pytest


pytest_plugins = 'sphinx.testing.fixtures'
collect_ignore = ['roots']


@pytest.fixture(scope='session')
def rootdir() -> Path:
    return Path(__file__).parent.abspath() / 'roots'
