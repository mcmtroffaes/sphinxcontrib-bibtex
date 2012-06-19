# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README", "rb") as readme_file:
    long_desc = readme_file.read()

with open("requirements.txt", "rb") as requires_file:
    requires = requires_file.read().split()

with open("VERSION", "rb") as version_file:
    version = version_file.read().strip()

setup(
    name='sphinxcontrib-bibtex',
    version=version,
    url='http://bitbucket.org/birkenfeld/sphinx-contrib',
    download_url='http://pypi.python.org/pypi/sphinxcontrib-bibtex',
    license='BSD',
    author='Matthias C. M. Troffaes',
    author_email='matthias.troffaes@gmail.com',
    description='Sphinx "bibtex" extension',
    long_description=long_desc,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    namespace_packages=['sphinxcontrib'],
)
