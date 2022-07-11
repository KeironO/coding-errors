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

from .standards import _build_standards_dict


def _check_rule_values(values, icd10s):

    mask_dict = {}

    for value in values:
        if value.endswith("X"):
            truth = [x.startswith(value[:-1]) for x in icd10s]
        elif len(value) == 3:
            truth = [x.startswith(value) for x in icd10s]
        else:
            truth = [value == x for x in icd10s]
        if True in truth:
            if value not in mask_dict:
                mask_dict[value] = []
            mask_dict[value].append(truth)

    return mask_dict

def _check_against_standard(returned_standard, icd10s):
    for standard, rules in returned_standard.items():
        for rule, values in rules.items():
            mask_dict = _check_rule_values(values, icd10s)
            

def run_check(icd10s: list, standards_dict = None):
    if standards_dict == None:
        standards_dict = _build_standards_dict()
    
    for icd10 in icd10s:
        if icd10 in standards_dict:
            returned_standard = standards_dict[icd10]
            result = _check_against_standard(returned_standard, icd10s)
            

    