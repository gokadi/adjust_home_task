#!/usr/bin/env python

from setuptools import setup

# Since we have pyproject.toml, this file is only needed for `--editable` mode
setup(
    setup_requires=[
        'setuptools>=30.4',
        'pip>=18.0',
    ],
    version='0.0.0'
)
