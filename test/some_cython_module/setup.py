from Cython.Build import cythonize
from setuptools import find_packages, setup

setup(
    name="some-cython-module",
    version="0.0.1",
    license="BSD",
    author="Matthias C. M. Troffaes",
    author_email="matthias.troffaes@gmail.com",
    description="Test module for bibtex citations in cython modules",
    zip_safe=False,
    platforms="any",
    packages=find_packages("src"),
    package_dir={"": "src"},
    ext_modules=cythonize(
        ["src/some_cython_module/cite.pyx", "src/some_cython_module/footcite.pyx"]
    ),
    python_requires=">=3.6",
)
