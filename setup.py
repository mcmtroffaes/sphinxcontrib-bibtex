import io
from setuptools import setup, find_packages
from typing import Optional


def readfile(filename):
    with io.open(filename, encoding="utf-8") as stream:
        return stream.read().split("\n")


readme = readfile("README.rst")[5:]  # skip title and badges
requires = readfile("requirements.txt")
version = readfile("VERSION")[0].strip()


# make entry point specifications
def plugin(plugin_name: str, mod_name: Optional[str] = None):
    if mod_name is None:
        mod_name = plugin_name
    path = "sphinxcontrib.bibtex.style.referencing"
    class_name = ''.join(part.capitalize() for part in plugin_name.split("_"))
    return f"{plugin_name} = {path}.{mod_name}:{class_name}ReferenceStyle"


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
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=requires,
    tests_require=['pytest', 'pytest-cov'],
    namespace_packages=['sphinxcontrib'],
    entry_points={
        'pybtex.style.names': [
            'last = sphinxcontrib.bibtex.style.names.last:LastNameStyle',
        ],
        'sphinxcontrib.bibtex.style.referencing': [
            plugin('author_year'),
            plugin('label'),
            plugin('super', 'super_'),
        ],
    }
)
