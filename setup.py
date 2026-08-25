# Thin setup.py for compatibility with tools that don't yet read pyproject.toml directly.
# All real package metadata lives in pyproject.toml -- see that file, and its note on why this
# repo has a setup.py at all despite an All Rights Reserved license (LICENSE).
from setuptools import setup

setup()
