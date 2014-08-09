#!/usr/bin/env python

from setuptools import setup
import json


with open("conf/options.json") as f:
    __options__ = json.load(f)


setup(
    name=__options__["general"]["name"],
    version=__options__["general"]["version"],
    description=__options__["general"].get("description", ""),
    long_description=open('README.md', 'rt').read(),
    author=__options__["general"].get("author", ""),
    url=__options__["general"].get("url", ""),
    include_package_data=True,
    install_requires=__options__["python"].get("install_requires", []),
    tests_require=__options__["python"].get("tests_require", []),
    extras_require={'test': __options__["python"].get("tests_require", [])},
    entry_points=__options__["python"].get("entry_points", []),
)
