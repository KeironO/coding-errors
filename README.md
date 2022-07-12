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
pip install git+https://github.com/KeironO/coding-errors --no-cache-dir
```


## Usage

```python
>>> from codingerrors import run
>>> run(["J440", "J22"])
{'DCS.X.5:0': {'!': {'pass': False, 'relevant': ['J22']}}}
```

### Standards

Currently, this little tool accounts for the following standards:

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
- DCS.IV.1: DM should be either Type 1/Type 2 or unknown
- DChS.XX.1: External Causes 
- DSC.XXII.5: COVID-19: B972 without U071, U071 must be in primary position, B972 should not directly follow codes in J18_, U049 SARS should not be coded, B342 or B972 should not directly follow U071 or U072…. This guidence from WHO and NHS Digital, U072 should not be coded with B342, Z115, Z038, U073 must not be assigned with U071 or U072, U073 must not be assigned with U074
- DChS.XVIII: Signs, symptoms and abnormal laboratory findings: abdomen pain should not be coded with appendicitis K35, K36,K37, chest pain should not be coded with I21, I22, shortness of breath should not be coded with Pneumonia (J12 - J18) or LRTI (J22) or IECOPD (J440)
- DChS.XI.1: Constipation with ileus or obstruction
- DChS.XIII.1: Musculoskeletal 5th Character
- DCS.XIV.5: no need to assign urethral obstruction N368 with N40X
- DSC.V.7: Z72.0 tobacco use must not be coded
- Four Step Coding Procedures : Neonatal Jaundice, B95/B96/B97/B98 never in primary position, I350 should not be coded with I351, I830 should not be coded with I831, K802 should not be coded with K81, Z721 should not be coded with F102, N13.2 Hydronephrosis with N20_

## Bug reporting and feature suggestions

Please report all bugs or feature suggestions to the [issues tracker](https://www.github.com/KeironO/coding-errors/issues). Please do not email me directly as I'm struggling to keep track of what needs to be fixed.

## License
Code is proudly released under the terms of the [MIT License](https://raw.githubusercontent.com/KeironO/coding-errors/main/LICENSE).

