# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import codecs

def readfile(filename):
    with codecs.open(filename, encoding="utf-8") as stream:
        return stream.read().split("\n")

doclines = readfile("README.rst")
requires = readfile("requirements.txt")
version = readfile("VERSION")[0].strip()

setup(
    name='sphinxcontrib-bibtex',
    version=version,
    url='https://github.com/mcmtroffaes/sphinxcontrib-bibtex',
    download_url='http://pypi.python.org/pypi/sphinxcontrib-bibtex',
    license='BSD',
    author='Matthias C. M. Troffaes',
    author_email='matthias.troffaes@gmail.com',
    description=doclines[0],
    long_description="\n".join(doclines[2:]),
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
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    namespace_packages=['sphinxcontrib'],
    use_2to3=True,
)
