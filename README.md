# ICD-10 Coding Evaluation

[![GitHub commits](https://badgen.net/github/commits/KeironO/coding-errors/main)](https://GitHub.com/KeironO/coding-errors/main/commit/)
![GitHub issues](https://img.shields.io/github/issues/KeironO/coding-errors)
![GitHub repo size](https://img.shields.io/github/repo-size/KeironO/coding-errors)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

This is a simple tool to evaluate a list of ICD-10 codes against DCS/DChS coding standards.

## Installation

You can install the development version directly from GitHub with:

```
pip install git+https://github.com/KeironO/coding-errors
```

### Standards

- DChS.II.2: Anaemia must not be coded in leukaemia, myeloma and myelodysplasia
- DCS.III.1: Sickle cell trait must not be coded with thalassaemia or sickle cell anaemia with or without crisis
- DCS.X.5: COPD with Chest infection, Chest infection and pneumonia, COPD with pneumonia, and COPD with Emphysema
- DCS.X.7: Respiratory Failure
- DCS.XI.4: Gastritis and duodenitis
- DCS.XV.14: Multiple gestation
- DCS.XI.5: Parastoma hernia
- DCS.V.3: Delirum and Dementia
- DCS.VI.2: Amaurosis fugax
- DCS.IX.10: Heart Failure CCF, and Pulmonary Oedema
- DCS.IX.14: Atherosclerosis
- DCS.XIX.2: Fifth character in Chapter XIX
- DCS.XXI.9: Palliative care

## Usage

```python
>>> from codingerrors import run
>>> run(["J440", "J22"])
{'DCS.X.5:0': {'!': {'pass': False, 'relevant': ['J22']}}}
```

## Bug reporting and feature suggestions

Please report all bugs or feature suggestions to the [issues tracker](https://www.github.com/KeironO/coding-errors/issues). Please do not email me directly as I'm struggling to keep track of what needs to be fixed.

## License
Code is proudly released under the terms of the [MIT License](https://raw.githubusercontent.com/KeironO/coding-errors/main/LICENSE).

