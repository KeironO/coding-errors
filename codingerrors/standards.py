# The MIT License
# 
# Copyright (c) 2022 Keiron O'Shea
# 
# Permission is hereby granted, free of charge, 
# to any person obtaining a copy of this software and 
# associated documentation files (the "Software"), to 
# deal in the Software without restriction, including 
# without limitation the rights to use, copy, modify, 
# merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom 
# the Software is furnished to do so, 
# subject to the following conditions:
# 
# The above copyright notice and this permission notice 
# shall be included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES 
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR 
# ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from .utils import hyph


# ! : Cannot be coded with
#   # : Unless present
# .n: Require's nth character
# { : Must always be coded with

standards_dict = {
    # Anaemia must not be coded in leukaemia, myeloma and myelodysplasia
    "DChS.II.2:0": "?D64:!C90-C95",
    # Sickle cell trait must not be coded with thalassaemia or sickle cell anaemia with or without crisis
    "DCS.III.1:0": "?D573:!D56,D570,D571",
    # COPD with Chest infection 
    "DCS.X.5:0": "?J440:!J22X",
    # Chest infection and pneumonia
    "DCS.X.5:1": "?J18:!J22",
    # COPD with pneumonia
    "DCS.X.5:2": "?J449:!J12-J18",
    # COPD with Emphysema
    "DCS.X.5:3": "?J449:!J439",
    # Respiratory Failure
    "DCS.X.7:0": "?J960,J961,J969:.5"
}


def _build_standards_dict() -> dict:
    compiled_standards_dict = {}
    for key, standard in standards_dict.items():
        standard = standard.split(":")

        primary_icd10s = hyph(standard[0][1:])
        
        for icd10 in primary_icd10s:
            
            if icd10 not in compiled_standards_dict:
                compiled_standards_dict[icd10] = {}

            for part in standard[1:]:
                dehyphyed = hyph(part[1:])
                if part.startswith("."):
                    if key not in compiled_standards_dict[icd10]:
                        compiled_standards_dict[icd10][key] = {}
                    compiled_standards_dict[icd10][key]["."] = part[1:]
                else:
                    if key not in compiled_standards_dict[icd10]:
                        compiled_standards_dict[icd10][key] = {}
                    compiled_standards_dict[icd10][key][part[0]] = dehyphyed

    return compiled_standards_dict
