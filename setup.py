#!/usr/bin/env python

import os
from setuptools import setup, find_packages


def parse_requirements_file(filename):
    return [
        r.strip()
        for r in open(os.path.join(os.getcwd(), filename)).readlines()
    ]


requirements = parse_requirements_file("src/requirements.txt")
test_requirements_dev = parse_requirements_file("requirements-dev.txt")

setup(
    name="Identity",
    description="Address Transaction",
    author="Next Caller Inc.",
    author_email="engineering@nextcaller.com",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=requirements,
    extras_require={"test": test_requirements_dev},
)
