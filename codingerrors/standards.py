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

# &* : Can never be in the primary position
# ^ : Must be in primary or secondary position.
# ? : Applies to the following codes.
# / : never code
# ! : Cannot be coded with
#   # : Unless present
# .n: Require's nth character
# { : Must always be coded with
# ~x..y: x character cannot be y

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
    "DCS.X.7:0": "?J960,J961,J969:.5",
    # Gastritis and duodenitis
    "DCS.XI.4:0": "?K297:!K298",
    # Multiple gestation
    "DCS.XV.14:0": "?O30:{Z372-Z377",
    # Parastoma hernia
    "DCS.XI.5:0": "?K433,K435:{Z93",
    # Delirum and Dementia
    "DCS.V.3:0": "?F03X,F01,F02:!F050,F059",
    # Amaurosis fugax
    "DCS.VI.2:0": "?G453:!H54",
    # Heart Failure CCF
    "DCS.IX.10:0": "?I501,I509:!I500,I50X",
    # Pulmonary Oedema
    "DCS.IX.10:1": "?I00-I01,I05-I10,I119,I12,I14-15,I20-I25,I25-I35,I38-I40,I49,I51,I52:!J81X",
    # Atherosclerosis 
    "DCS.IX.14:0": "?I70:.5",
    # Fifth character in Chapter XIX
    "DCS.XIX.2:0": "?S02,S12,S22,S32,S42,S52,S62,S72,S82,S92,T02,T08,T10,T12:.5",
    # Palliative care
    "DCS.XXI.9:0": "?Z518:!Z515",
    # DM should be either Type 1/Type 2 or unknown
    "DCS.IV.1:0": "?E11,E14:!E10",
    "DCS.IV.1:1": "?E11:!E14,E10",
    "DCS.IV.1:2": "?E14:!E10,E11",
    # External Causes 
    "DChS.XX.1:0": "?V01-V99,Y01-Y98:&*",
    # B972 without U071 
    "DSC.XXII.5:COVID-19:0": "?U071:!B972",
    # Signs, symptoms and abnormal laboratory findings
    "DChS.XVIII:0": "?G40,G41;!R568",
    # Constipation with ileus or obstruction
    "DChS.XI.1:0": "?K56,K400,K403,K413,K420,K430,K433,K436,K440,K450,K460:!K590",
    # Musculoskeletal 5th Character
    "DChS.XIII.1:0": "?M00-M25,M40-M54,M60-M99:~5..9",
    # no need to assign urethral obstruction N368 with N40X
    "DCS.XIV.5:0" :"?N40X:!N368",
    # Z72.0 tobacco use must not be coded
    "DSC.V.7:0": "?Z720:/*",
    
    # Neonatal Jaundice 
    "FSCP:0": "?P072,P073:!P599",
    # B95/B96/B97/B98 Never in primary position
    "FSCP:1": "?B95-B98:&*",
    # I350 should not be coded with I351
    "FSCP:2": "?I351:!I350",
    # I080 coded with codes from I34 and I35
    "FSCP:3": "?I34,I35:!I080",
    # M479 should not be coded with 5th character of 2 cervical, 6 lumbar or 8 sacral
    "FSCP:4": "?M4792, M4796,M4798:/*",
    # Z722 should not be coded with F55, F19, F11,F12,F13,F14,F15,F16
    "FSCP:5": "?F55,F19,F11,F12,F13,F14,F15,F16:!Z722",
    # Z720 should not be coded with F171
    "FSCP:6": "?F171:!Z720",
    # I350 should not be coded with I351
    "FSCP:7": "?I351:!I350",
    # I830 should not be coded with I831
    "FSCP:8": "?I831:!I830",
    # K802 should not be coded with K81
    "FSCP:9": "?K81:!K802",
    # Z721 should not be coded with F102
    "FSCP:10": "?F102:!Z721",
    # N13.2 Hydronephrosis with N20_
    "FSCP:11": "?N132:!N20"
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
                elif part[0] in ("&", "/"):
                    if key not in compiled_standards_dict[icd10]:
                        compiled_standards_dict[icd10][key] = {}
                    compiled_standards_dict[icd10][key][part[0]] = icd10
                elif part[0] == "~":
                    character, have = part[1:].split("..")
                    if key not in compiled_standards_dict[icd10]:
                        compiled_standards_dict[icd10][key] = {}
                    compiled_standards_dict[icd10][key][part[0]] = {
                        "character": character,
                        "have": have
                    }
                else:
                    if key not in compiled_standards_dict[icd10]:
                        compiled_standards_dict[icd10][key] = {}
                    compiled_standards_dict[icd10][key][part[0]] = dehyphyed
    return compiled_standards_dict
