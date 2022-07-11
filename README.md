# Coding Dashboard Error Checker

[![GitHub commits](https://badgen.net/github/commits/KeironO/coding-dashboard-errors/main)](https://GitHub.com/KeironO/coding-dashboard-errors/main/commit/)
![GitHub issues](https://img.shields.io/github/issues/KeironO/coding-dashboard-errors)
![GitHub repo size](https://img.shields.io/github/repo-size/KeironO/coding-dashboard-errors)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

This is a simple tool to evaluate a list of ICD-10 codes against DCS/DChS coding standards.

## Installation

You can install the development version directly from GitHub with:

```
pip install git+https://github.com/KeironO/coding-dashboard-errors

```

## Usage

```python
>>> from codingerrors import run
>>> run(["J440", "J22"])
{'DCS.X.5:0': {'!': {'pass': False, 'relevant': ['J22']}}}
```

## Bug reporting and feature suggestions

Please report all bugs or feature suggestions to the [issues tracker](https://www.github.com/KeironO/coding-dashboard-errors/issues). Please do not email me directly as I'm struggling to keep track of what needs to be fixed.

## License
Code is proudly released under the terms of the [MIT License](https://raw.githubusercontent.com/KeironO/coding-dashboard-errors/main/LICENSE).

