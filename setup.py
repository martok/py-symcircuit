#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    packages=find_packages(),
    name="SymCircuit",
    version="0.1.0",
    url="https://github.com/martok/py-symcircuit",
    author="Martok",
    author_email="martok@martoks-place.de",
    description="Symbolic electronic circuit analysis",
    license="MIT",
    classifiers=[
    ],
    install_requires=[
        "sympy",
    ],
    python_requires='>=3.6',
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
    extras_require={
        "EE": [
            "networkx",
            "numpy",
            "plotkit"
        ],
    }
)
