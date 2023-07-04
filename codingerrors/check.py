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
                    if True in list(itertools.chain(*mask)):
                        if standard not in results:
                            results[standard] = {}
                        rel = [icd10s[x.index(True)] for x in mask]
                        results[standard][rule] = {
                            "pass": False,
                            "relevant": rel,
                            "note": "You cannot code %s with %s"
                            % ("".join(rel), icd10),
                        }

            elif rule == "€":
                primary_code_position = icd10s.index(icd10)
                if True in list(
                    itertools.chain(*list(itertools.chain(*list(mask_dict.values()))))
                ):
                    for code, mask in mask_dict.items():
                        if True in list(itertools.chain(*mask)):
                            if primary_code_position != (
                                list(itertools.chain(*mask)).index(True) + 1
                            ):
                                rel = [icd10s[x.index(True)] for x in mask]
                                results[standard] = {
                                    "pass": False,
                                    "relevant": icd10,
                                    "note": "%s can only exist after %s"
                                    % (icd10, "/".join(rel)),
                                }
                else:
                    if standard not in results:
                        results[standard] = {}

                    results[standard][rule] = {
                        "pass": False,
                        "relevant": icd10,
                        "note": "%s cannot exist without one of %s"
                        % (icd10, "/".join(values)),
                    }
            
            elif rule == "£":

                primary_code_position = icd10s.index(icd10)

                for key, value in mask_dict.items():
                    for v in value:
                        if True in v:
                            pos = v.index(True)

                            if pos > primary_code_position:
                                if standard not in results:
                                    results[standard]= {}
                                results[standard][rule] = {
                                    "pass": False,
                                    "relevant": icd10,
                                    "note": "%s cannot be coded before %s"
                                    % (icd10, key),
                                }

                        

            elif rule == "¿":
                tim = [
                    True in list(itertools.chain(*_mask))
                    for k, _mask in mask_dict.items()
                ]
                if False not in tim:
                    # If both are present
                    proper_pos = False
                    pos = icd10s.index(icd10)

                    for code, mask in mask_dict.items():
                        if mask[0].index(True) == (pos - 1):
                            proper_pos = True
                    if not proper_pos:
                        if standard not in results:
                            results[standard] = {}
                        rel = list(mask_dict.keys())

                        results[standard][rule] = {
                            "pass": False,
                            "relevant": rel,
                            "note": "%s must be coded after one of %s when %s are all present"
                            % (icd10, "/".join(rel), "/".join(rel)),
                        }

            elif rule == ")":
                primary_code_position = icd10s.index(icd10)

                for code, mask in mask_dict.items():
                    tim = list(itertools.chain(*mask))
                    if True in tim:
                        index = tim.index(True)
                        if index != (primary_code_position + 1) and index != (
                            primary_code_position - 1
                        ):
                            if standard not in results:
                                results[standard] = {}
                            rel = [icd10s[x.index(True)] for x in mask]
                            results[standard][rule] = {
                                "pass": False,
                                "relevant": rel,
                                "note": "%s must be coded before or after %s"
                                % (icd10, "".join(rel)),
                            }

            elif rule == "¬":
                primary_code_position = icd10s.index(icd10)

                if primary_code_position == 0:
                    for code, mask in mask_dict.items():
                        tim = list(itertools.chain(*mask))
                        if True in tim:
                            index = tim.index(True)
                            if index == (primary_code_position + 1):
                                if standard not in results:
                                    results[standard] = {}
                                rel = [icd10s[x.index(True)] for x in mask]
                                results[standard][rule] = {
                                    "pass": False,
                                    "relevant": rel,
                                    "note": "When %s in primary poition it cannot be followed by %s"
                                    % (icd10, ", ".join(rel)),
                                }
            elif rule == "$":
                position = icd10s.index(icd10)

                if mask_dict == {}:
                    if standard not in results:
                        results[standard] = {}
                    results[standard][rule] = {
                        "pass": False,
                        "rel": icd10s,
                        "note": "%s missing?"
                        % (" or ".join(returned_standard[standard][rule])),
                    }
                else:
                    for code, mask in mask_dict.items():
                        _mask = list(itertools.chain(*mask))
                        if _mask.index(True) != position - 1:
                            if standard not in results:
                                results[standard] = {}

                            rel = [icd10s[x.index(True)] for x in mask]

                            results[standard][rule] = {
                                "pass": False,
                                "relevant": rel,
                                "note": "%s must always follow %s"
                                % (icd10, " or ".join(rel)),
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
                        "note": "%s needs to have a %i character"
                        % (icd10, int(values)),
                    }
            elif rule == "/":
                if standard not in results:
                    results[standard] = {}
                results[standard][rule] = {
                    "pass": False,
                    "relevant": [icd10],
                    "note": "%s cannot be coded" % icd10,
                }

            elif rule == ">":
                primary_code_position = icd10s.index(icd10)
                for code, masks in mask_dict.items():
                    for mask in masks:
                        if True in mask:
                            mask_positions = mask.index(True)
                            if type(mask_positions) == int:
                                if mask_positions == primary_code_position + 1:
                                    if standard not in results:
                                        results[standard] = {}
                                    results[standard][rule] = {
                                        "pass": False,
                                        "relevant": [icd10],
                                        "note": "%s should not be coded directly after %s"
                                        % (code, icd10),
                                    }

            elif rule == "<":
                error = False

                if "&" in icd10:
                    splits =  icd10.split("&")
                    for index, i in enumerate(icd10s):
                        if i == splits[0]:
                            if icd10s[index:len(splits)] == splits:
                                primary_code_position = index+len(splits)-1
                else:
                    primary_code_position = icd10s.index(icd10)
                

                if mask_dict == {}:
                    error = True
                for code, masks in mask_dict.items():
                    for mask in masks:
                        if True in mask:
                            mask_positions = [
                                i for i, x in enumerate(mask) if x == True
                            ]

                            if primary_code_position + 1 not in mask_positions:
                                error = True
                        else:
                            error = False
                    if error == False:
                        break

                if error:
                    if standard not in results:
                        results[standard] = {}
                    
                    if len(values) > 1:
                        note = "One of %s needs to coded directly after %s" % (",".join(values), icd10)
                    else:
                        note = "%s needs to be coded directly after %s" % (values[0], icd10)
                    
                    results[standard][rule] = {
                        "pass": False,
                        "relevant": [icd10],
                        "note": note
                    }

            elif rule == "~":
                character = int(values["character"])
                have = values["have"]
                passes = True
                if len(icd10) >= character:
                    if icd10[character - 1] == have:
                        passes = False

                if not passes:
                    if standard not in results:
                        results[standard] = {}

                    results[standard][rule] = {
                        "pass": False,
                        "relevant": [icd10],
                        "note": "%s has %s in the %i position"
                        % (icd10, have, character),
                    }

            elif rule == "&":
                if icd10 == icd10s[0]:
                    if standard not in results:
                        results[standard] = {}
                    results[standard][rule] = {
                        "pass": False,
                        "relevant": [icd10],
                        "note": "%s cannot be in primary position!" % (icd10),
                    }
            elif rule == "^":
                rule_pass = False

                if len(icd10s) == 1:
                    rule_pass = True

                elif icd10 in icd10s[0:2]:
                    rule_pass = True

                if not rule_pass:
                    if standard not in results:
                        results[standard] = {}

                        results[standard][rule] = {
                            "pass": False,
                            "relevant": [icd10],
                            "note": "%s must be in primary or secondary position!"
                            % (icd10),
                        }

    # Exception clauses (@)
    for standard, rules in returned_standard.items():
        if "@" in rules and standard in results:
            exception_codes = rules["@"]

            mask_dict = _check_rule_values(values, icd10s)

            # 🤡 <- Me writing this code.
            if True in itertools.chain(
                *list(itertools.chain(*list(mask_dict.values())))
            ):
                del results[standard]

    return results
