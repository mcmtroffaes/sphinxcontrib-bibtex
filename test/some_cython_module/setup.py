from setuptools import Extension, setup

setup(
    ext_modules=[
        Extension(
            name="some_cython_module.cite",
            sources=["src/some_cython_module/cite.pyx"],
        ),
        Extension(
            name="some_cython_module.footcite",
            sources=["src/some_cython_module/footcite.pyx"],
        ),
    ]
)
