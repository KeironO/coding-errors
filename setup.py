#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md")) as f:
    long_description = f.read()

setup(
    name="codingerrors",
    version="0.1.2",
    description="Coding Dashboard Error Checker",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KeironO/coding-dashboard-errors",
    author="KeironO",
    author_email="keiron.oshea@wales.nhs.uk",
    packages=find_packages(),
    include_package_data=True,
)
