#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name="src",
    version="1.0",
    packages=find_packages(),
    entry_points={"console_scripts": ["manage=manage:main"]},
)
