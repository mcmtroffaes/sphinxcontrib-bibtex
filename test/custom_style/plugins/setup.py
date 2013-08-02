# run "python setup.py egg_info"

from setuptools import setup

setup(
    name='plugins',
    version='0.1.0',
    entry_points={
        'pybtex.style.formatting': [
            'nowebref = plugins:NoWebRefStyle',
        ]
    },
    py_modules=['plugins']
)
