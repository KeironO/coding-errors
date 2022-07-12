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
            truth = [x == value[:-1] for x in icd10s]
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
                        rel = [icd10s[x.index(True)] for x in mask]
                        results[standard][rule] = {
                            "pass": False,
                            "relevant": rel,
                            "note": "You cannot code %s with %s" % ("".join(rel), icd10),
                        }
            elif rule == "{":

                if mask_dict == {} or True not in list(
                    itertools.chain(
                        *[list(itertools.chain(*v)) for v in mask_dict.values()]
                    )
                ):
                    if standard not in results:
                        results[standard] = {}
                    results[standard][rule] = {
                        "pass": False,
                        "relevant": [icd10],
                        "note": "None of %s found" % (",".join(values)),
                    }
            elif rule == ".":
                if len(icd10) < int(values):
                    if standard not in results:
                        results[standard] = {}
                    results[standard][rule] = {
                        "pass": False,
                        "relevant": [icd10],
                        "note": "%s needs to have a %i character" % (icd10, int(values)),
                    }
            elif rule == "/":
                if standard not in results:
                    results[standard] = {}
                results[standard][rule] = {
                    "pass": False,
                    "relevant": [icd10],
                    "note": "%s cannot be coded" % icd10
                }

            elif rule == ">":
                primary_code_position = icd10s.index(icd10)
                for code, masks in mask_dict.items():
                    for mask in masks:
                        if True in mask:
                            mask_positions = mask.index(True)

                            if type(mask_positions) == int:
                                if mask_positions == primary_code_position+1:
                                    if standard not in results:
                                        results[standard] = {}
                                    results[standard][rule] = {
                                        "pass": False,
                                        "relevant": [icd10],
                                        "note": "%s should not be coded directly after %s" % (code, icd10)
                                    }

            elif rule == "~":
                character = int(values["character"])
                have = values["have"]
                passes = True
                if len(icd10) >= character:
                    if icd10[character-1] == have:
                        passes = False

                if not passes:
                    if standard not in results:
                        results[standard] = {}
                    
                    results[standard][rule] = {
                        "pass": False,
                        "relevant": [icd10],
                        "note": "%s has %s in the %i position" % (icd10, have, character)
                    }

            elif rule == "&":
                if icd10 == icd10s[0]:
                    if standard not in results:
                        results[standard] = {}
                    results[standard][rule] = {
                        "pass": False,
                        "relevant": [icd10],
                        "note": "%s cannot be in primary position!" % (icd10)
                    }
    return results
