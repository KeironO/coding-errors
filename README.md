# UK Clinical Coding Quality Check

[![GitHub commits](https://badgen.net/github/commits/KeironO/coding-errors/main)](https://GitHub.com/KeironO/coding-errors/main/commit/)
![GitHub issues](https://img.shields.io/github/issues/KeironO/coding-errors)
![GitHub repo size](https://img.shields.io/github/repo-size/KeironO/coding-errors)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

This is a simple tool to evaluate a list of clinically coded codes (ICD-10 and OPCS4) against evaluate them against a number of coding standards.

Coding standards currently implemented are:

- National Clinical Coding Standards ICD-10 5th Edition (2021)
- National Clinical Coding Standards OPCS-4 (2021)

## Installation

You can install the development version directly from GitHub with:

```
pip install git+https://github.com/KeironO/coding-errors --no-cache-dir
```

## Usage

```python
>>> from codingerrors import run
>>> run(["J440", "J22"])
{'J440': {'DCS.X.5:0:E': {'!': {'pass': False, 'relevant': ['J22'], 'note': 'You cannot code J22 with J440'}}}}
```

## Standards

Currently, this little tool accounts for the following standards:

### National Clinical Coding Standards ICD-10 5th Edition (2021)

- **DCS.I.5 : Zika Virus** :: Ensure that U06.9 (Emergency use of U06.9) is correctly sequenced with A92.8 (Other specified mosquito-borne viral fevers). Please note that this includes the pregnancy positioning, without checking for whether O98.5 (Other viral diseases complicating pregnancy , childbirth and the puerperium) is present.
- **DChS.XVI.1 : Liveborn infants acording to place of birth** :: When a Z38 (Liveborn infants according to place of birth) is assigned, it must always be in the primary diagnosis or secondary position. Please not that this does not check to see whether the baby is completely not well, it just assumes that a code in secondary position is due to this.
- **DCS.XV.19 : Morbidly adherent placenta** :: O43.2 (Morbidly adherent placenta) must be assigned following either O72.0 (Third-stage haemorrhage) or O73.0 (Retained placenta and membranes, without haemorrhage) when both are present.
- **DCS.XVI.7 : Stillbirths** :: P95.X (Fetal death of unspecified cause) is not required in any
diagnostic position.

### Four Step Coding Principles (ICD-10)

## Contributors

- Lisa Cartwright
- Claire Connell
- Joanne Gapper
- Keiron O'Shea 

## Bug reporting and feature suggestions

Please report all bugs or feature suggestions to the [issues tracker](https://www.github.com/KeironO/coding-errors/issues).

## License
Code is proudly released under the terms of the [MIT License](https://raw.githubusercontent.com/KeironO/coding-errors/main/LICENSE).

![cwm taf logo](https://img.keiron.xyz/ru59p3.png)

