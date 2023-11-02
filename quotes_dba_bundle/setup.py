"""
setup.py configuration script describing how to build and package this project.

This file is primarily used by the setuptools library and typically should not
be executed directly. See README.md for how to deploy, test, and run
the quotes_dba_bundle project.
"""
from setuptools import setup, find_packages

import sys
sys.path.append('./src')

import quotes_dba_bundle

setup(
    name="quotes_dba_bundle",
    version=quotes_dba_bundle.__version__,
    url="https://databricks.com",
    author="d.martins@kigroup.de",
    description="wheel file based on quotes_dba_bundle/src",
    packages=find_packages(where='./src'),
    package_dir={'': 'src'},
    entry_points={
        "packages": [
            "main=quotes_dba_bundle.main:main"
        ]
    },
    install_requires=[
        # Dependencies in case the output wheel file is used as a library dependency.
        # For defining dependencies, when this package is used in Databricks, see:
        # https://docs.databricks.com/dev-tools/bundles/library-dependencies.html
        "setuptools"
    ],
)
