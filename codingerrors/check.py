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

import itertools
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

def _check_against_standard(returned_standard, icd10s, icd10):
    results = {}
    for standard, rules in returned_standard.items():
        for rule, values in rules.items():
            mask_dict = _check_rule_values(values, icd10s)
            if rule == "!":
                
                for code, mask in mask_dict.items():
                    if standard not in results:
                            results[standard] = {}
                    if True in list(itertools.chain(*mask)):
                        results[standard][rule] = {"pass": False, "relevant": [icd10s[x.index(True)] for x in mask], "note": None}
            elif rule == "{":
                
                if mask_dict == {} or True not in list(itertools.chain(*[list(itertools.chain(*v)) for v in mask_dict.values()])):
                    if standard not in results:
                            results[standard] = {}
                    results[standard][rule] = {"pass": False, "relevant": [], "note": "None of %s found" % (",".join(values))}
            elif rule == ".":
                 if len(icd10) < int(values):
                        if standard not in results:
                            results[standard] = {}
                        results[standard][rule] = {"pass": False, "relevant": [icd10], "note": None}
    return results
            



    