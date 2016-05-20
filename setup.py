# -*- coding: utf-8 -*-

import io
from setuptools import setup, find_packages
import sys


def readfile(filename):
    with io.open(filename, encoding="utf-8") as stream:
        return stream.read().split("\n")

readme = readfile("README.rst")[5:]  # skip title and badges
requires = readfile("requirements.txt")
version = readfile("VERSION")[0].strip()

if sys.version_info < (2, 7):
    requires.append('ordereddict>=1.1')

setup(
    name='sphinxcontrib-bibtex',
    version=version,
    url='https://github.com/mcmtroffaes/sphinxcontrib-bibtex',
    download_url='https://pypi.python.org/pypi/sphinxcontrib-bibtex',
    license='BSD',
    author='Matthias C. M. Troffaes',
    author_email='matthias.troffaes@gmail.com',
    description=readme[0],
    long_description="\n".join(readme[2:]),
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    namespace_packages=['sphinxcontrib'],
)
