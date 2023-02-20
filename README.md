# UK Clinical Coding Quality Check

[![GitHub commits](https://badgen.net/github/commits/KeironO/coding-errors/main)](https://GitHub.com/KeironO/coding-errors/main/commit/)
![GitHub issues](https://img.shields.io/github/issues/KeironO/coding-errors)
![GitHub repo size](https://img.shields.io/github/repo-size/KeironO/coding-errors)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

This is a simple tool to evaluate a list of clinically coded codes (ICD-10 and OPCS4) against evaluate them against a number of coding standards.

Coding standards currently implemented are:

- National Clinical Coding Standards ICD-10 5th Edition (2022)
- National Clinical Coding Standards OPCS-4 (2022)

## Installation

You can install the development version directly from GitHub with:

```
pip install git+https://github.com/KeironO/coding-errors --no-cache-dir
```

## Usage

### ICD-10

```python
>>> from codingerrors import run
>>> run(["J440", "J22"])
{'J440': {'DCS.X.5:0:E': {'!': {'pass': False, 'relevant': ['J22'], 'note': 'You cannot code J22 with J440'}}}}
```

### OPCS-4

```python
>>> from codingerrors import run
>>> run(["M676", "M707"], type="opcs4")
```

python
>>> from codingerrors import run
>>> run(["J440", "J22"], )
{'J440': {'DCS.X.5:0:E': {'!': {'pass': False, 'relevant': ['J22'], 'note': 'You cannot code J22 with J440'}}}}

## Contributors

- Lisa Cartwright
- Claire Connell
- Joanne Gapper
- Ewelina Tetlak
- Keiron O'Shea 

## Bug reporting and feature suggestions

Please report all bugs or feature suggestions to the [issues tracker](https://www.github.com/KeironO/coding-errors/issues).

## License
Code is proudly released under the terms of the [MIT License](https://raw.githubusercontent.com/KeironO/coding-errors/main/LICENSE).

![cwm taf logo](https://img.keiron.xyz/ru59p3.png)

