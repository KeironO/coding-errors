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

from gzip import READ
from .standards import _build_standards_dict
from .check import _check_against_standard

from .utils import chunks
from .standards import icd10_standards_dict, opcs4_standards_dict




def run(icd10s: list, type: str = "icd10", standards_dict: dict = None):
    if standards_dict != None:
        pass
    elif type.upper() == "ICD10":
        standards_dict = _build_standards_dict(icd10_standards_dict)
    elif type.upper() == "OPCS4":
        standards_dict = _build_standards_dict(opcs4_standards_dict)

    final_results = {}

    

    for icd10 in icd10s:

        if icd10 not in final_results:
            final_results[icd10] = {}

        # Check against X codes. This is where we have a hard limit of 3 characters.
        if len(icd10) == 3:
            if "%sX" % (icd10) in standards_dict:
                final_results[icd10] = _check_against_standard(
                    standards_dict["%sX" % (icd10)], icd10s, icd10
                )

        if icd10 in standards_dict:
            results = _check_against_standard(standards_dict[icd10], icd10s, icd10)

            for standard, result in results.items():
                final_results[icd10][standard] = result

        if len(icd10) > 3 and icd10[0:3] in standards_dict:
            results = _check_against_standard(standards_dict[icd10[0:3]], icd10s, icd10)

            for standard, result in results.items():
                final_results[icd10][standard] = result

    for index in range(len(icd10s)+1)[::-1]:
        if index == 0:
            continue

        for chunk in chunks(icd10s, index):
            chunk = [x for x in chunk if x != None]

            if len(chunk) == 1:
                continue
            
            icd10_chunk = '&'.join(chunk)

            if icd10_chunk in standards_dict:
                results = _check_against_standard(standards_dict[icd10_chunk], icd10s, icd10_chunk)

                if icd10_chunk not in final_results:
                    final_results[icd10_chunk] = {}
                
                for standard, result in results.items():
                    final_results[icd10_chunk][standard] = result

        
    for k in [k for k, v in final_results.items() if v == {}]:
        del final_results[k]

    return final_results
