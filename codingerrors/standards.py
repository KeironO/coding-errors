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


###  First sequence

# ? : Applies to the following codes.
## If a single code is matched, it will be evaluated by the contents of the following sequences.


### Second sequence

# &* : Can never be in the primary position
## Any or all of the codes in the first sequence can never, under any circumstance be in primary position.

# ^* : Must be in primary or secondary position.
## Any or all of the codes in the first sequence must always be in primary or secondary position.

# / : never code
## Any of the codes in the first sequence can never, under any circumstance be coded.

# ! : Cannot be coded with
## Any or all of the codes in the first sequence should never be coded with the following codes, in any position.

# .n: Require's nth character
## Any or all of the codes in the first sequence require a nth character.

# { : Must always be coded with
##

# ~x..y : x character cannot be y

# > : Should not be directly followed by

# ¿ :

# % : Outpatient only codes

# $ : Should always follow by

# € : Can only exist when coded after one of...

# ) : Should always be sequences either way by

# ¬ : When in primary position should never be followed by

## Third sequence
# @ : Ignore the 'error' if any of the following codes are present.


icd10_standards_dict = {
    # ☑️ Zika Virus (U068) must always be followed by other specified Mosquito-borne viral fever (A929)
    # Amendment: Where <, add the secondary code.
    "DCS.I.5:0:E": "?U068:<A928",
    # Metastatic cancer must have a primary cancer or history of a primary cancer
    # Amendment: Can't really make it up, so ignore or add a Z85.
    "DCS.II.2:0:E": "?C77-C79:{C00-C76,C80,Z85,D329",
    # ☑️ A (Z38) must be primary or first secondary diag position
    # Amendment: Move to the front of the codes unless suited for secondary.
    "DChS.XVI.1:0:E": "?Z38:^*",
    # ☑️ Only code O432 AFTER O720/O730
    # O43.2 (Morbidly adherent placenta) must be assigned following either O72.0 (Third-stage haemorrhage) or O73.0
    # (Retained placenta and membranes, without haemorrhage) when both are present.
    # Amendment: Place O432 between one of O720 or O730
    # 05/09/2022: This is wrong. Need to write a check for when both codes are present that O432 is actually there.
    # "DCS.XV.19:0:E": "?O432:¿O720,O730",
    # ☑️ Fetal death of unspecified cause (P95) should not coded  is not requird in any diagnostic position .
    # Amendment: Take forward for further evaluation, but not working with obstretics.
    "DCS.XVI.7:0:E": "?P95X:/*",
    # ☑️ Malignant neoplasms of independent (primary) multiple sites (C97X) should always be coded in the primary
    # diagnosis position. Additional codes must be used
    # Amendment: Move  C97X to the primary position.
    "DCS.II.4:0:E": "?C97X:^*",
    # Failed trial of labour, unspecified (O664) and Failed application of vacuum extractor and forceps (O665)
    # should not be coded.
    # Amendment: Take forward for future evaluation.
    "DSC.XV.24W:0:W": "?O664,O665:/*",
    # This was asked for by Joanne Gapper, to differentiate between a given warning and an actual data quality error.
    # Abnormality of forces of labour (O629) and Long labour (O63) cannot be coded with Failed trial of labour,
    # unspecified (O664) or Failed application of vacuum extractor and forceps (O665)
    # Amendment: Bring forward for further analysis.
    "DSC.XV.24E:0:E": "?O664,O665:!O629,O63",
    # Diabetes mellitus (E10-E14) should not be coded in an obstetric clinical episode (where O00-O99 denotes a likely episode)
    # Amendment: Remove Diabetes code, and replace with a relevant code within Diabetes mellitus in pregnancy, childbirth
    # and the puerperium (O24)
    "DCS.XV.9:0:E": "?O00-O99:!E10,E11,E14",
    # Mental and behavioural disorders due to use of alcohol (F100) should not be coded with any codes in Poisoning by drugs,
    # medicaments and biological substances (T36-T50), unless Toxic effect of alcohol : Ethanol (T510) is also assigned.
    # Amendment: Remove the F100 code.
    "DCS.XIX.8:0:E": "?F100:!T36-T50:@T510",
    # Malignant neoplasms, stated or presumed to be primary, of lymphoid, haematopoietic and related tissue (C81-C96) should
    # not be coded with any of Secondary and unspecified malignant neoplasm of lymph nodes (C77), Secondary malignant neoplasm
    # of respiratory and digestive organs (C78), or Secondary malignant neoplasm of other and unspecified sites (C79) unless
    # there is a code from Malignant neoplasms, stated or presumed to be primary, of specified sites, except of lymphoid,
    # haematopoietic and related tissue (C00 to C75) or Malignant neoplasm, without specification of site (C80) or
    # Personal history of malignant neoplasm (Z85) are present.
    # Amendment: Bring forward for future analysis. We're not focusing too much on stuff that describes cancer.
    "DCS.II.7:0:E": "?C81-C96:!C77-C79:@C00-C75,C80,Z85",
    # Outcome of delivery codes such as between Twins, both liveborn (Z372) and Other multiple births, all stillborn (Z377)
    # are intended for use as an additional code to identify the outcome of delivery on the mother's record and should always
    # be coded as part of a Multiple gestation (O30).
    # Amendment: Bring forward for future analysis.
    "DCS.XV.14:0:E": "?Z372-Z377:{O30",
    # If present, dementia in Alzheimer disease (F00) must always either be sequenced directly before or after a
    # code from Alzheimer disease (G30)
    # Amendment: If G30 not present, add a Alzheimer disease, unspecified (G309).
    "DGCS.5:0:E": "?F00:)G30",
    # When present, Systemic Inflammatory Response Syndrome of infectious origin with organ failure (R651) must always be
    # coded directly following one of Streptococcal sepsis (A40), Other sepsis (A41), Bacterial sepsis of newborn (P36),
    # Puerperal sepsis (O85), Septicaemic plague (A207), Generalized tularaemia (A217), Anthrax sepsis(A227), Brucellosis,
    # unspecified (A239), Erysipelothrix sepsis (A267), Extraintestinal yersiniosis (A282), Listerial sepsis (A327),
    # Waterhouse-Friderichsen syndrome (A391), Actinomycotic sepsis (A427), Other gonococcal infections (A548), Candidal
    # sepsis (B377), Other infection during labour (O753), or Meningococcaemia, unspecified (A394)
    # Amendment: Remove R651 if none of the required codes are present.
    "DChS.I.1:0:E": "?R651:€A40,A41,P36,O85,A207,A217,A227,A239,A267,A282,A327,A391,A427,A548,B377,O753,A394",
    # If any codes within Persons with potential health hazards related to communicable diseases excluding Need for other
    # prophylactic measures (Z29) (Z20-Z28) are placed in the primary position, they shuld not be directly followed by any
    # codes within A00-B99 and R00-T99.
    # Amendment: Reposition code so that the rule passes.
    "DCS.XXI.3:0:E": "?Z20-Z28:¬A00-A99,B00-B99,R00-R99,S00-S99,T00-T99",
    # Other anaemias (D64) cannot not be coded in codes Multiple myeloma and malignant plasma cell neoplasms
    # (C90), Lymphoid leukaemia (C91), Myeloid leukaemia (C92), Monocytic leukaemia (C93), Other leukaemias of specified
    # cell type (C94), or Leukaemia of unspecified cell type (C95).
    # Amendment: Remove anemia code as it's a given for leukemia.
    "DChS.II.2:0:E": "?D64:!C90-C95",
    # When present, Sickle-cell trait (D573) cannot be coded with any of Thalassaemia (D56), or Sickle-cell anaemia with
    # crisis (D570), or Sickle-cell anaemia without crisis (D571).
    # Amendment: Remove Sickle-cell trait (D573) when codes are present.
    "DCS.III.1:0:E": "?D56:!D573",
    "DCS.III.1:1:E": "?D570:!D573",
    "DCS.III.1:2:E": "?D571:!D573",
    # DCS.X.5: COAD/COPD, chest infection and asthma with associated conditions is quite a large standard that needs to be
    # broken up into a number of parts. Chronic obstructive pulmonary disease with acute lower respiratory infection
    # (J440) should not be coded with a Unspecified acute lower respiratory infection (J22).
    # Amendment: Remove the J22 as J440 already denotes that the lower respiratory infection is present.
    # "DCS.X.5:0:E": "?J440:!J22",
    # Chronic obstructive pulmonary disease, unspecified (J449) should not be coded with J22X.
    # Amendment: Change J449 to J440 to denote that it's COPD with an acute lower respiratory infection, and remove J22X.
    # "DCS.X.5:1:E": "?J449:!J22",
    # Chest infection and pneumonia
    # "DCS.X.5:2:W": "?J18:!J22",
    # COPD with pneumonia
    # "DCS.X.5:3:E": "?J449:!J12-J18",
    # Emphysema (J43) cannot be coded with Chronic obstructive pulmonary disease (J44). J43 describes emphysemic episodes.
    # Amendment: Remove the J44.
    # "DCS.X.5:4:E": "?J43:!J44",
    "DCS.X.5:0:E": "?J440:!J22X",
    # Chest infection and pneumonia
    "DCS.X.5:1:W": "?J18:!J22",
    # COPD with pneumonia
    "DCS.X.5:2:E": "?J449:!J12-J18",
    # COPD with Emphysema
    "DCS.X.5:3:E": "?J449:!J439",
    # All codes in Respiratory failure (J960) should always be coded to the fifth character.
    # Amendment: If a fifth character is not present, add a 9.
    "DCS.X.7:0:E": "?J960,J961,J969:.5",
    # The standard specifies that Gastroduodenitis, unspecified (K299) should only be assigned if the episode has both
    # (K297) and Duodenitis (K298) are present. From this a DQ error is thrown if both are present.
    # Amendment: Replace both with Gastroduodenitis (K299).
    "DCS.XI.4:0:E": "?K297:!K298",
    # A code from Artifical Opening Status (Z93) must be assigned when any of Parastomal hernia with obstruction, without
    # gangrene (K433), Parastomal hernia with gangrene (K434), or Parastomal hernia without obstruction or gangrene (K435)
    # Amendment: Add a Artificial opening status, unspecified (Z939) if no record of stoma is present.
    "DCS.XI.5:0:E": "?K433,K434,K435:{Z93",
    # There is no need to code a formal diagnosis of Unspecified dementia (F03X) when Delirium superimposed on dementia (F051)
    # is present.
    # Amendment: Remove F03X.
    "DCS.V.3:0:E": "?F051:!F03X",
    # It has been advised that all codes within Mental and behavioural disorders due to multiple drug use and use of other
    # psychoactive substances (F19) should not be coded besides all codes within  Mental and behavioural disorders due to
    # psychoactive substance use (F10-19) excluding F19, and Mental and behavioural disorders due to use of tobacco (F17)
    # Amendment: Remove F10-16 and F-18 codes.
    "DCS.V.4:0:W": "?F19:!F10-F16,F18",
    # The standard states that no additional code should be assigned to classify loss of vision in patients who have been
    # diagnosed with Amaurosis fugax (G453) as this is implict within the code. A common error we've found is that people
    # are coding Visual impairment including blindness (binocular or monocular) (H53), so we check this here.
    # Amendment: Remove the Visual impairment including blindness (binocular or monocular) (H53) codes.
    "DCS.VI.2:0:E": "?G453:!H54",
    # I23.- Certain current complications following acute myocardial infarction must not be coded with I21.- or I22.-
    "DCS.IX.6:0:E": "?I21,I22:!I23",
    # I46.9 unspecified cardiac arrest should not be coded with I46.0 or I46.1
    "DCS.IX.8:0:E ": "?I460,I461:!I469",
    # Heart Failure CCF
    "DCS.IX.10:0:E": "?I501,I509:!I500,I50X",
    # Pulmonary Oedema
    "DCS.IX.10:1:E": "?I00-I01,I05-I10,I119,I12,I14-15,I20-I25,I25-I35,I38-I40,I49,I51,I52:!J81X",
    # congestive cardiac failure (CCF) (I50.0) should not be coded with left ventricular failure (LVF) (I50.1)
    "DCS.IX.10:2:E": "?I501:!I500",
    # I64.X Stroke, must not be coded with I63.-
    "DCS.IX.11:0:E": "?I64X:!I63",
    # Atherosclerosis
    "DCS.IX.14:0:E": "?I70:.5",
    # Fifth character in Chapter XIX
    "DCS.XIX.2:0:E": "?S02,S12,S22,S32,S42,S52,S62,S72,S82,S92,T02,T08,T10,T12:.5",
    # Palliative care # LC YOU CAN CODE THEM TOGETHER, IF THE Z51.8 IS BEING USED TO IDENTIFY OTHER MEDICAL CARE BUT NEVER IN D01*
    "DCS.XXI.9:0:W": "?Z518:!Z515",
    # DM should be either Type 1/Type 2 or unknown
    "DCS.IV.1:0:E": "?E11,E14:!E10",
    "DCS.IV.1:1:E": "?E11:!E14,E10",
    "DCS.IV.1:2:E": "?E14:!E10,E11",
    # External Causes
    "DChS.XX.1:0:E": "?V01-V99,Y01-Y98:&*",
    # B972 without U071
    "DSC.XXII.5:COVID-19:0:W": "?U071:>B972",
    # U071 coded with U072
    "DSC.XXII.5:COVID-19:1:E": "?U071:!U072",
    # U071 must be in primary position - Removed on the 28th September 2022.
    # "DSC.XXII.5:COVID-19:2:W": "?U071:^*",
    # B972 should not directly follow codes in J18_
    "DSC.XXII.5:COVID-19:3:E": "?J18:>B972",
    # South Asian Respiratory Syndrome (U049) should not be coded in any circumstance.
    # Amendment: Remove the U049.
    "DSC.XXII.5:COVID-19:4:E": "?U049:/*",
    # B342 or B972 should not directly follow U071 or U072…. This guidence from WHO and NHS Digital
    "DSC.XXII.5:COVID-19:5:E": "?U071,U072:>B342",
    # U072 should not be coded with B342, Z115, Z038
    "DSC.XXII.5:COVID-19:6:E": "?U072:!B342,Z115,Z038",
    # U073 must not be assigned with U071 or U072
    "DSC.XXII.5:COVID-19:7:E": "?U071,U072:!U073",
    # U073 must not be assigned with U074
    "DSC.XXII.5:COVID-19:8:E": "?U074:!U073",
    # Signs, symptoms and abnormal laboratory findings
    "DChS.XVIII:0:W": "?G40,G41:!R568",
    # R10 - abdomen pain should not be coded with appendicitis K35, K36,K37
    "DChS.XVIII:1:E": "?K35-K37:!R10",
    # R07 - chest pain should not be coded with I21, I22
    "DChS.XVIII:2:E": "?I21-I22:!R07",
    # R060 - shortness of breath should not be coded with Pneumonia (J12 - J18) or LRTI (J22) or IECOPD (J440)
    "DChS.XVIII:3:E": "?J12-J18:!R060",
    # R568 should not be coded with either G40 or G41
    "DChS.XVIII:4:W": "?G40-G41:!R568",
    # R251 should not be coded with either G20 or G21
    "DChS.XVIII:5:E": "?G20-G21:!R251",
    # Constipation with ileus or obstruction
    "DChS.XI.1:0:E": "?K56,K400,K403,K413,K420,K430,K433,K436,K440,K450,K460:!K590",
    # Musculoskeletal 5th Character
    "DChS.XIII.1:0:E": "?M00-M25,M40-M54,M60-M99:~5..9",
    # no need to assign urethral obstruction N368 with N40X
    "DCS.XIV.5:0:E": "?N40X:!N368",
    # Z72.0 tobacco use must not be coded                                                          FOR CURRENT SMOKER USE F17.1
    "DSC.V.7:0:E": "?Z720:/*",
    # Z12.1 Special screening examination for neoplasm of intestinal tract
    "DCS.XXI.1:0:E": "?D12,K55-K64,C18-C21:!Z121",
    # Y838 and Y839 and Y848 and Y849 should not be coded with a code from T80-T88
    "DSC.XIX.7:0:E": "?T80-T88:!Y838,Y839,Y848,Y849",
    # N993 should not be directly followed by Y83/Y84
    "DCS.XIV.12:0:E": "?N993:>Y83,Y84",
    # F80 should not be coded with either F81 or F82
    "DCS.XIV.12:1!E:": "?F81,F82:!F80",
    # CKD with Renal Failure
    "DCS.XIV.2:0:E": "?N184,N185:!N19",
    # Chronic kidney disease
    "DCS.XIV.2:1:E": "?N182,N183,N184,N185,N189:!N181",
    "DCS.XIV.2:2:E": "?N181,N183,N184,N185,N189:!N182",
    "DCS.XIV.2:3:E": "?N181,N182,N184,N185,N189:!N183",
    "DCS.XIV.2:4:E": "?N181,N182,N183,N185,N189:!N184",
    "DCS.XIV.2:5:E": "?N181,N182,N183,N184,N189:!N185",
    "DCS.XIV.2:6:E": "?N181,N182,N183,N184,N185:!N189",
    # T29 should not be coded
    "DCS.XIX.5:0:E": "?T29:/*",
    # J95.8 should not be coded
    "DSC.XIX.7:1:W": "?J958:/*",
    # Codes O95, O96, O97 should never be assigned
    "DCS.XV.29:0:E": "?O95-O97:/*",
    # D649 should not be coded with O990
    "DSC.XV.32:0:E": "?O990:!D649",
    # Geriatric and elderly falls (R296)
    "DCS.XVIII.4:0:E": "?R296:>W00-W19",
    # Sepsis codes should not be followed by B95 or B96
    "DCS.I.4:0:E": "?A40,A41:>B95,B96",
    # R69.X/R96.X/R98.X/R99.X should not be coded is other information is available for code assignment
    "DCS.XVIII.11:0:E": "?R69X,R96X,R98X,R99X:/*",
    # Rare Delivery Codes
    "DCS.XV.28:0:W": "?O801,O802,O808,O809,O81,O821,O822,O828,O829,O83,O84:/*",
    # Delivery
    "DCS.XV.28:1:E": "?O10-O16,O20-O48,O60-O75,O85-O92,O94-O99:!O800,O820",
    # Code M16.-, M17.-, M18.- AND M19.- must not be coded together, M15.- must be coded instead to indicate multiple areas of osteoarthritis.
    "DCS.XII.2:0:E": "?M16:!M17,M18,M19",
    "DCS.XII.2:1:E": "?M17:!M16,M18,M19",
    "DCS.XII.2:2:E": "?M18:!M16,M17,M19",
    "DCS.XII.2:3:E": "?M19:!M16,M17,M18",
    # I13.- must not be coded with I11.- or I12.-
    "DCS.IX.2:0:E": "?I11-I12:?I13",
    # T795 should not be coded with N179
    "DCS.XIII.3:0:E": "?N179:!T795",
    # Severe Sepsis : R65.1 must always be coded directly following a code from A40._ or A41._or P36._ or O85. or (A207,A217,A227,A239,A267,A282,A327,A391,A427,A548,B377,O753 - have added A394)
    # "DChS.I.1:0:E": "?A40,A41,P36,O85,A207,A217,A227,A239,A267,A282,A327,A391,A427,A548,B377,O753:<R651",
    # I739 should not be coded with I702,I723,I724,I743,I744,I745
    "DC.IX.15:0:E": "?I702,I723,I724,I743,I744,I745:!I739",
    # K22.2 must not be coded with Q39.4
    "DCS.XI.1:0:E": "?Q394:!K222",
    # Haemorrhoids
    "DCS.XI.10:0:E": "?K641,K642,K643:!K640",
    "DCS.XI.10:1:E": "?K640,K642,K643:!K641",
    "DCS.XI.10:3:E": "?K640,K641,K643:!K642",
    "DCS.XI.10:4:E": "?K640,K641,K642:!K643",
    # Pressure Ulcers
    "DCS.XII.3:0:E": "?L891,L892,L893,L899:!L890",
    "DCS.XII.3:1:E": "?L890,L892,L893,L899:!L891",
    "DCS.XII.3:2:E": "?L890,L891,L893,L899:!L892",
    "DCS.XII.3:3:E": "?L890,L891,L892,L899:!L893",
    "DCS.XII.3:4:E": "?L890,L891,L892,L893:!L899",
    # Infected Pressure Ulcers
    "DCS.XII.3:5:E": "?L89,L97X:>B95,B96",
    # Arthrosis
    "DChS.XIII.2:0:E": "?M17,M19:!M16",
    "DChS.XIII.2:1:E": "?M19,M16:!M17",
    "DChS.XIII.2:2:E": "?M17,M16:!M19",
    # N20.2  must not be coded with N20.0 or N20.1
    "DCS.XIV.3:0:E": "?N200,N201:!N202",
    # Neoplasia Prostate
    "DCS.XIV.7:0:E": "?D075,C61X:!N423",
    "DCS.XIV.7:1:E": "?N423,C61X:!D075",
    "DCS.XIV.7:2:E": "?D075,N423:!C61X",
    # CIN
    "DCS.XIV.10:0:E": "?N871,N879,D069:!N870",
    "DCS.XIV.10:1:E": "?D069,N870,N879:!N871",
    "DCS.XIV.10:2:E": "?N870,N871,N879:!D069",
    "DCS.XIV.10:3:E": "?N870,N871,D069:!Z879",
    # VAIN
    "DCS.XIV.10:4:E": "?N891,N899,D072:!N890",
    "DCS.XIV.10:5:E": "?D072,N890,N899:!N891",
    "DCS.XIV.10:6:E": "?N890,N891,N899:!D072",
    "DCS.XIV.10:7:E": "?N890,N891,D072:!N899",
    # O20.- must not be coded with O00.-, O01.-, o02.-, o03.-, o04.-, o05.- o06.-, o07.-, o08.-
    "DCS.XV.6:0:E": "?O08-O08:!020",
    # O21.- must not be coded with R11.x
    "DCS.XV.7:0:E": "?021:!R11",
    # Z33.x must not be used with any code from O00.- to O99.-
    "DCS.XXI.5:0:E": "?O00-O99:!Z33",
    # Pregnant state, incidental
    "DCS.XV.33:0:E": "?Z33X:&*",
    # Dehydration of newborn (P74.1) must not be coded with E86.x
    "DCS.IV.7:0:E": "?E86X:!P741",
    # R68.8 must not be coded with N17.-, k72.9, i50.-, i51.- or any other organ failure code
    "DCS.XVIII.10:0:E": "?N17,K729,I50,I51:!R688",
    # Fetus and newborn affected by maternal factors and by complications of pregnancy, labour and delivery
    "DCS.XVI.1:0:E": "?P00-P04:&*",
    # H54.0 Blindness, binocular (if unspecified or stated of both eyes) must not be coded with H54.4 Blindness, monocular (if stated to be of one eye only).
    "DCS.VII.3:0:E": "?H544:!H540",
    # H91.9 must not be coded with H90.0, h90.1, h90.2, h90.3, h90.4, h90.5, h90.6, h90.7, h90.8, h91.0, h91.1, h91.2, h91.3, h91.8
    "DCS.VIII.1:0:E": "?H90,H910,H911,H912,H913,H918:!H919",
    # Neonatal Jaundice
    "FSCP:0:E": "?P072,P073:!P599",
    # B95/B96/B97/B98 Never in primary position
    "FSCP:1:E": "?B95-B98:&*",
    # I350 should not be coded with I351
    "FSCP:2:E": "?I351:!I350",
    # I080 coded with codes from I34 and I35
    "FSCP:3:E": "?I34,I35:!I080",
    # M479 should not be coded with 5th character of 2 cervical, 6 lumbar or 8 sacral
    "FSCP:4:E": "?M4792,M4796,M47968:/*",
    # Z720 should not be coded with F171
    "FSCP:6:E": "?F171:!Z720",
    # I350 should not be coded with I351                                                                                      SEE FSCP:2:E
    "FSCP:7:E": "?I351:!I350",
    # I830 should not be coded with I831
    "FSCP:8:E": "?I831:!I830",
    # K802 should not be coded with K81
    "FSCP:9:E": "?K81:!K802",
    # Z721 should not be coded with F102
    "FSCP:10:E": "?F102:!Z721",
    # N13.2 Hydronephrosis with N20_
    "FSCP:11:E": "?N132:!N20",
    # I633-I634-I635 should not be coded with I65
    # "FSCP:12:E": "?I65:!I633-I635", <- To investigate
    # J852 Abscess of lung without pneumonia should not be coded with pneumonia
    "FSCP:13:W": "?J12-J18:!J852",
    # I080 coded with codes from I34 and I35
    "FSCP:14:E": "?I34-I35:!I080",
    # codes O640 - O663 should not be coded with O320 - O324/O326 -O329 and O33._
    "FSCP:15:E": "?O320-O324,O326-O329,O33:!O640-O663",
    # Dementia
    "FSCP:16:E": "?F03:!F01-F02",
    # R251 should not be followed directly by a code between Y40 - Y59
    "FSCP:17:E": "?R251:>Y40-Y59",
    # M109 should not be directly followed by a code from Y40-Y59
    "FSCP:18:E": "?M109:>Y40-Y59",
    # E162 should not be directly followed by a code from Y40-Y59
    "FSCP:19:E": "?E162:>Y40-Y59",
    # R51X should not be directly followed by code from Y40 - Y59
    "FSCP:20:E": "?R51X:>Y40-Y59",
    # S271 should not be coded with S270
    "FSCP:21:E": "?S271:!S270",
    # A09, K520, K522,K523,K528,K529 should not be directly followed by a code from Y40 - Y59
    "FSCP:22:E": "?A09:>K520,K522,K523,K528,K529:>Y40-Y59",
    # M102,E242,M804,L640,E273,E160,G251,G720,N141,D592,E661,M814,K853,L105,M342,E064,G256,G444,M835 should be directly followed by code from Y40 - Y59
    "FSCP:23:E": "?M102,E242,M804,L640,E273,E160,G251,G720,N141,D592,E661,M814,K853,L105,M342,E064,G256,G444,M835:<Y40-Y59",
    # G620 not directly followed by a code from Y40-Y59 or Y880
    "FSCP:24:E": "?G620:>Y40-Y59,Y880",
    # Codes L233/L251/L270/L271 should be followed by a code from Y10-Y599 to state what drug caused the dermatitis
    "FSCP:25:E": "?L233,L251,L270,L271:{Y10-Y58,Y599",
    # Chronic diarrhoea with infective diarrhoea
    "FSCP:26:W": "?A09:!K529",
    # J18 should not be followed by a code by B95 and B96
    "FSCP:27:E": "?J18:>B95,B98",
    # I959 should not be directly followed by a code from Y40-Y59
    "FSCP:28:E": "?I959:>Y40-Y59",
    # K859 should not be directly followed by a code from Y40-Y59
    "FSCP:29:E": "?K859:>Y40-Y59",
    # G629 should not be directly followed by a code from Y40-Y59
    "FSCP:30:E": "?G629:>Y40-Y59",
    # B95 B96 should not directly follow I830
    "FSCP:31:E": "?I830:>B95,B96",
    # Kidney and Ureter Calculi
    "FSCP:32:E": "?N201,N202:!N200",
    # Codes from L30 should not be directly followed by any codes in the range Y100 - Y599
    "FSCP:33:E": "?L30:>Y10-Y59",
    # Influenza with pneumonia
    "FSCP:34:W": "?J13-J18:!J10-J11",
    # Ankylosis of joint should not be coded with stiffness of joint
    "FSCP:35:E": "?M256:!M246",
    # K802 Calculus of gallbladder without cholecystitis coded with K81_ Cholecystitis
    "FSCP:36:E": "?K81:!K802",
    # I260 should not be coded with I279
    "FSCP:37:E": "?I279:!I260",
    # I95.2 Hypotension due to drugs should have an additional Y40 - Y59 coded directly beneath
    "FSCP:38:E": "?I952:<Y40-Y59",
    # Z21X coded with symptomatic HIV
    "FSCP:39:E": "?B20-B24:!Z21X",
    # Perineal laceration during delivery
    "FSCP:40:E": "?O701,O704-O709:!O700,0702,0703",
    # Codes from I64 should not be coded with I63
    "FSCP:41:E": "?I63:!I64",
    # I630-I631-I632 should not be coded with I65
    "FSCP:42:E": "?I65:!I630-I632",
    # Type 1 errors
    "T1:001:X": "?A182:!A163,A183",
    "T1:002:X": "?A40:!O05,O03,O07,T814,T802,T880,O06,O04,O85X,O080,O753",
    "T1:003:X": "?A41:!A40,O05,O03,O07,A499,T814,A393,T802,T880,O06,A548,O04,O753,O080,O85X",
    "T1:004:X": "?A56:!P231",
    "T1:005:X": "?A74:!A56,A55,P231",
    "T1:006:X": "?B00:!P352",
    "T1:007:X": "?C49:!C50,C46,C41,C40,C300,C323,C48",
    "T1:008:X": "?D69:!M311,D891,D890,D65X",
    "T1:009:X": "?D72:!R72X,D82,D83,D80,D70X,D81,D89,D86,D88,D84,D87,D758,D85",
    "T1:010:X": "?D76:!I898",
    "T1:011:X": "?D89:!R771",
    "T1:012:X": "?E53:!E648",
    "T1:013:X": "?E54:!E642",
    "T1:014:X": "?F04:!F116,F126,F156,F136,F166,F186,F440,F176,F146,F196",
    "T1:015:X": "?F061:!R401",
    "T1:016:X": "?F070:!F072,F621,F071,F620",
    "T1:017:X": "?F20:!F252,F232",
    "T1:018:X": "?F31:!F30",
    "T1:019:X": "?F32:!F920,F33",
    "T1:020:X": "?F45:!F984,F808",
    "T1:021:X": "?F440:!F116,F126,F156,R412,F166,F186,R413,R411,F176,F146",
    "T1:022:X": "?F442:!R401,F202",
    "T1:023:X": "?F511:!G471",
    "T1:024:X": "?F602:!F91",
    "T1:025:X": "?F630:!Z726",
    "T1:026:X": "?F631:!F00,Z032",
    "T1:027:X": "?F632:!F00,Z032,F32",
    "T1:028:X": "?F800:!R470,H91,R482,H90",
    "T1:029:X": "?F801:!F802,F803,R470",
    "T1:030:X": "?F802:!F803,H91,F801,R470,H90",
    "T1:031:X": "?F812:!R488,F813",
    "T1:032:X": "?F91:!F92",
    "T1:033:X": "?F98:!G478",
    "T1:034:X": "?F930:!F931,F932",
    "T1:035:X": "?F941:!F942,Z615,Z614,Z616",
    "T1:036:X": "?F942:!F941",
    "T1:037:X": "?F982:!R633",
    "T1:038:X": "?F984:!F02,G24,G21,G23,R25,F04,G22,F00,F03,F05",
    "T1:039:X": "?G04:!G934",
    "T1:040:X": "?G08:!I676",
    "T1:041:X": "?G44:!R51X",
    "T1:042:X": "?G52:!H491",
    "T1:043:X": "?G570:!M543",
    "T1:044:X": "?G70:!P940",
    "T1:045:X": "?G72:!M332,M622,M33,M60",
    "T1:046:X": "?G91:!P917,P371",
    "T1:047:X": "?H025:!G256",
    "T1:048:X": "?H27:!Z961",
    "T1:049:X": "?H40:!H445,P153",
    "T1:050:X": "?H46:!H470",
    "T1:051:X": "?H49:!H525",
    "T1:052:X": "?H59:!Z961",
    "T1:053:X": "?H81:!R42X",
    "T1:054:X": "?I08:!I35,I34,I38X,I38,I37,I091,I36",
    "T1:055:X": "?I21:!I258,I23",
    "T1:056:X": "?I31:!I092,I970,I23",
    "T1:057:X": "?I34:!I059,I058,I05,I080,I050",
    "T1:058:X": "?I36:!I07",
    "T1:059:X": "?I37:!I098",
    "T1:060:X": "?I38:!I091,I424",
    "T1:061:X": "?I46:!R570",
    "T1:062:X": "?I49:!P291",
    "T1:063:X": "?I50:!I971,I110,P290,I13",
    "T1:064:X": "?I72:!I60",
    "T1:065:X": "?I74:!I634,I24,I22,I631,I23",
    "T1:066:X": "?I770:!Q273",
    "T1:067:X": "?I80:!G08X,I821,I870,G951,I676,K751",
    "T1:068:X": "?I82:!I636,I676,I21,I26,I25,I80,I81X,I24,G951,I22,K550,G08X,I23",
    "T1:069:X": "?I88:!R59,L04",
    "T1:070:X": "?I89:!I972,R59,N508",
    "T1:071:X": "?I95:!R579,R031",
    "T1:072:X": "?J00:!J303,J302,J304,J02,J029",
    "T1:073:X": "?J02:!J36X,J391,J390,J060",
    "T1:074:X": "?J04:!J05",
    "T1:075:X": "?J040:!J111,J101,J09X",
    "T1:076:X": "?J09:!G000,J10,J14X",
    "T1:077:X": "?J10:!G000,J09X,J14X",
    "T1:078:X": "?J11:!G000,J14X",
    "T1:079:X": "?J12:!J849,J100,U049,P350,J09X,J110,P230",
    "T1:080:X": "?J15:!J160,P23",
    "T1:081:X": "?J16:!J189,P23",
    "T1:082:X": "?J18:!J851,J849,J702,J841,J703,J704",
    "T1:083:X": "?J20:!J40X,J450",
    "T1:084:X": "?J371:!J42X",
    "T1:085:X": "?J43:!P250,J983,J44,J982,J684",
    "T1:086:X": "?J82:!M30,M35,J702,M36,M32,M34,M31,J703,J704,M33",
    "T1:087:X": "?J84:!J982",
    "T1:088:X": "?J90:!R091,J940",
    "T1:089:X": "?J93:!P251,J86",
    "T1:090:X": "?J94:!R091",
    "T1:091:X": "?J98:!R068,P284,P283",
    "T1:092:X": "?J986:!Q790,Q791",
    "T1:093:X": "?K07:!K108",
    "T1:094:X": "?K12:!K130",
    "T1:095:X": "?K14:!K132",
    "T1:096:X": "?K004:!A505",
    "T1:097:X": "?K122:!K052",
    "T1:098:X": "?K56:!K551,K44,K45,K624,K315,K43,K42,K46,E841,K40,K913,K41",
    "T1:099:X": "?K59:!F453,K90,R194",
    "T1:100:X": "?K62:!K512,K914",
    "T1:101:X": "?K630:!K57",
    "T1:102:X": "?K631:!K57,K26",
    "T1:103:X": "?K632:!K316,N823",
    "T1:104:X": "?K65:!N735,K57,P781,N734,P780,N733,K35,E850",
    "T1:105:X": "?K72:!K704,K711,P59,P58,P56,P57,P55",
    "T1:106:X": "?K73:!K71,K752,K753,K701",
    "T1:107:X": "?K75:!K73,K720",
    "T1:108:X": "?K83:!K915",
    "T1:109:X": "?K830:!K804,K750,K803",
    "T1:110:X": "?L04:!I881,I889,I880,R59",
    "T1:111:X": "?L022:!N61X,P38X",
    "T1:112:X": "?L12:!L401",
    "T1:113:X": "?L23:!L309,T784,L259",
    "T1:114:X": "?L24:!L309,T784,L259",
    "T1:115:X": "?L25:!L309,T784,L24,L23",
    "T1:116:X": "?L27:!T784,T887,L24",
    "T1:117:X": "?L29:!F458",
    "T1:118:X": "?L30:!I832,L24,I831",
    "T1:119:X": "?L233:!T887",
    "T1:120:X": "?L251:!T887",
    "T1:121:X": "?L50:!L563,P838,T806,L23,D841,L282,T783",
    "T1:122:X": "?L67:!L650",
    "T1:123:X": "?L95:!M052,M793,M540,T806,L817,D690,L932,L50",
    "T1:124:X": "?L97:!I830,I832,R02X",
    "T1:125:X": "?L984:!I832,R02X",
    "T1:126:X": "?M19:!M15",
    "T1:127:X": "?M20:!Z89",
    "T1:128:X": "?M21:!Z89",
    "T1:129:X": "?M23:!M932,M22,M246,M244,M221,M21,M220",
    "T1:130:X": "?M24:!K076",
    "T1:131:X": "?M216:!M203,M202,M205,M204",
    "T1:132:X": "?M242:!M357,M237,M238,M236",
    "T1:133:X": "?M245:!M720,M671",
    "T1:134:X": "?M246:!M256",
    "T1:135:X": "?M40:!M41,M96",
    "T1:136:X": "?M41:!I271,M96",
    "T1:137:X": "?M43:!M80,M81,M88",
    "T1:138:X": "?M432:!M45X",
    "T1:139:X": "?M45:!M081,M023",
    "T1:140:X": "?M674:!A666",
    "T1:141:X": "?M70:!M719",
    "T1:142:X": "?M77:!M719",
    "T1:143:X": "?M715:!M719",
    "T1:144:X": "?M86:!K102",
    "T1:145:X": "?M95:!K07",
    "T1:146:X": "?M96:!M81,Z95",
    "T1:147:X": "?N06:!N392,N391,R80X",
    "T1:148:X": "?N19:!I120",
    "T1:149:X": "?N81:!N834,N993",
    "T1:150:X": "?N89:!N952,N76",
    "T1:151:X": "?N90:!N76",
    "T1:152:X": "?N95:!E283,N924",
    "T1:153:X": "?N816:!N813",
    "T1:154:X": "?N99:!M811,M801,N953",
    "T1:155:X": "?O22:!O02,O05,O03,O01,O07,O06,O04,O00,O087",
    "T1:156:X": "?O29:!O02,O05,O03,O01,O07,O06,O04,O08,O00",
    "T1:157:X": "?O31:!O65,O337,O325,O64,O66",
    "T1:158:X": "?O67:!O45,O44,O46",
    "T1:159:X": "?O85:!O883",
    "T1:160:X": "?O864:!O85X",
    "T1:161:X": "?O98:!R75X,Z21X",
    "T1:162:X": "?O99:!O98",
    "T1:163:X": "?O994:!O903",
    "T1:164:X": "?O997:!O268",
    "T1:165:X": "?O998:!O860,O862,O908,O863",
    "T1:166:X": "?P002:!P008",
    "T1:167:X": "?P041:!Q862,Q861",
    "T1:168:X": "?P52:!P10,P005",
    "T1:169:X": "?P83:!P394,P56,L00X",
    "T1:170:X": "?Q15:!H55X,H355",
    "T1:171:X": "?Q18:!K07,Q870,Q75",
    "T1:172:X": "?Q27:!Q281,Q282,Q256",
    "T1:173:X": "?Q28:!Q257,I608,I72,Q245",
    "T1:174:X": "?Q82:!L05,Q858",
    "T1:175:X": "?Q86:!E01",
    "T1:176:X": "?R00:!P291,I48",
    "T1:177:X": "?R07:!B330,J029,M542,R13X",
    "T1:178:X": "?R10:!N23X",
    "T1:179:X": "?R11:!P920,F505,O21,K910",
    "T1:180:X": "?R22:!R93,E65X,R190,R90,R91,R59,R60,R92,M254",
    "T1:181:X": "?R53:!T732,F480,F430,R54X,G933,T67,O268,T733",
    "T1:182:X": "?R71:!D750,D53,D50,D45X,D54,D52,D51,D751",
    "T1:183:X": "?S01:!S18X",
    "T1:184:X": "?S021:!S028",
    "T1:185:X": "?S023:!S028",
    "T1:186:X": "?S23:!M51",
    "T1:187:X": "?S33:!O716,M51",
    "T1:188:X": "?S48:!T116",
    "T1:189:X": "?S51:!S58",
    "T1:190:X": "?S81:!S88",
    "T1:191:X": "?S88:!T136",
    "T1:192:X": "?T20:!T28",
    "T1:193:X": "?T43:!T423,T407,T408,T426,T505,T409,T424",
    "T1:194:X": "?T465:!T501",
    "T1:195:X": "?T67:!L56,T21,L58,L57,L590,T883,L59",
    "T1:196:X": "?T68:!T885,R680,P80,T35",
    "T1:197:X": "?T69:!T35",
    "T1:198:X": "?T75:!T78,T21",
    "T1:199:X": "?T781:!A05",
    "T1:200:X": "?T79:!P22",
    "T1:201:X": "?T81:!T83,T887,T84",
    "T1:202:X": "?T88:!T83,T84",
    "T1:203:X": "?T802:!B17,B19,B16,B18,T846",
    "T1:204:X": "?T806:!B17,B18",
    "T1:205:X": "?T814:!T846",
    "T1:206:X": "?T817:!O02,T790,O05,O00,O01,O03,O07,O082,T838,O06,O04,T858,O88",
    "T1:207:X": "?T818:!T885",
    "T1:208:X": "?T881:!G040",
    "T1:209:X": "?W13:!W20X",
    "T1:210:X": "?W25:!W07,W03,W02,W09,W04,W00,W08,W01,W05,W06",
    "T1:211:X": "?W45:!W46X,W21,W28",
    "T1:212:X": "?X36:!V09,V08,V06,X34,V02,V07,V04,V03,V05",
    "T1:213:X": "?Z00:!Z02,Z12",
    "T1:214:X": "?Z01:!Z03,Z02,Z12",
    "T1:215:X": "?Z014:!Z305,Z32",
    "T1:216:X": "?Z36:!Z35",
    "T1:217:X": "?Z43:!Z45,K914,N995,J950,Z93",
    "T1:218:X": "?Z46:!Z96",
    "T1:219:X": "?Z47:!T84,Z50",
    "T1:220:X": "?Z48:!Z47,Z45",
    "T1:221:X": "?Z63:!Z61",
    "T1:222:X": "?Z90:!D730",
    # "T1:223:X": "?Z91:!Z864,Z58",
    "T1:224:X": "?Z96:!T83,Z45,T84",
    "T1:225:X": "?Z97:!Z44,T82,Z45,T83,T85,Z46,T84",
    "T1:226:X": "?Z867:!I69",
    "T1:227:X": "?Z875:!Z35",
}


opcs4_standards_dict = {
    # Pain relief procedure coding: Block of the brachial plexus.
    # Injection of therapeutic substance around peripheral nerve (A735) must be coded
    # with Brachial plexus NEC (Z089)
    "PCSA2:0:W": "?A735:{Z089",
    #
    "PCSA2:1:E": "?A573,A574,A575:{Z07",
    "PCSA2:2:W": "?V55:{Z00-Z99",
    "PCSA2:3:E": "?A111,A112:€A114",
    "PCSU3:0:E": "?B164:!Y93,Y94,Y97,Y98",
    "PChSV1:0:E": "?V22-V70:{V55",
    # Chapter A: Nervous System
    "002PLAC:0:E": "?A05:!A221,A40",
    "003PLAC:0:E": "?A064:!A391",
    "004PLAC:0:E": "?A113:!A203",
    "005PLAC:0:E": "?A281:!E137,E124",
    "006PLAC:0:E": "?A391:!A064",
    "007PLAC:0:E": "?A515:!A39",
    "008PLAC:0:E": "?A52:!Y89",
    "009PLAC:0:E": "?A736:!A71",
    "010PLAC:0:E": "?A841:!A11,U221",
    # Chapter B: Endocrine System and Breast
    "011PLAC:0:E": "?B30:!B312",
    "012PLAC:0:E": "?B39:!B293",
    "013PLAC:0:E": "?B45:!B312",
    # Chapter C: Eye
    "014PLAC:0:E": "?C09:!C151,C152",
    "015PLAC:0:E": "?C16:!C20",
    "016PLAC:0:E": "?C32,C33:!C31",
    "017PLAC:0:E": "?C52:!C532",
    "018PLAC:0:E": "?C80:!C841,C842",
    "019PLAC:0:E": "?C82:!C88",
    "020PLAC:0:E": "?C867:!C084,C434,C893",
    "021PLAC:0:E": "?C85:!C812",
    "022PLAC:0:E": "?C87:!C866,C865,A822,A845",
    "023PLAC:0:E": "?C825,C826:!C812",
    "024PLAC:0:E": "?C841:!C80",
    "025PLAC:0:E": "?C845:!C553",
    "026PLAC:0:E": "?C893:!C867",
    "027PLAC:0:E": "?C90:&*",
    "028PLAC:0:E": "?C90:!Y80",
    # Chapter D: Ear
    "029PLAC:0:E": "?D013:!D021",
    "030PLAC:0:E": "?D03:!X031",
    "031PLAC:0:E": "?D05:!D13",
    "032PLAC:0:E": "?D13:!D05",
    "033PLAC:0:E": "?D153:!D151",
    # Chapter E: Respiratory Tract
    "034PLAC:0:E": "?E02:/*",
    "035PLAC:0:E": "?E023,E024:!E073",
    "036PLAC:0:E": "?E124:!E137",
    "037PLAC:0:E": "?E147:!E162",
    "038PLAC:0:E": "?E25:!E65",
    "039PLAC:0:E": "?E36:!E37",
    "040PLAC:0:E": "?E41:!E42",
    "041PLAC:0:E": "?E441:!E442",
    "043PLAC:0:E": "?E24:!E253,E259,E64",
    "044PLAC:0:E": "?E32:!E369,E379",
    "045PLAC:0:E": "?E35:!E369,E379",
    "046PLAC:0:E": "?E35:!E369,E3710",
    "047PLAC:0:E": "?E48:!E499",
    "048PLAC:0:E": "?E50:!E519",
    "049PLAC:0:E": "?E62:!E639",
    "050PLAC:0:E": "?E64:!E659",
    "051PLAC:0:E": "?E893:!E855",
    "052PLAC:0:E": "?E931,E932:!E941",
    "053PLAC:0:E": "?E933,E934:!E492",
    "054PLAC:0:E": "?E551:!E59,E491",
    "055PLAC:0:E": "?E53:!K01",
    "056PLAC:0:E": "?E64:!E24",
    "057PLAC:0:E": "?E65:!E25",
    "058PLAC:0:E": "?E855:!E893",
    "059PLAC:0:E": "?E856:!X522",
    "060PLAC:0:E": "?E87:!X52",
    # Chapter F: Mouth
    "061PLAC:0:E": "?F03:!V123,V124",
    "062PLAC:0:E": "?F11:!V151",
    "063PLAC:0:E": "?F13:!F17",
    "064PLAC:0:E": "?F14:!F65-F66",
    "065PLAC:0:E": "?F19:!V151",
    "066PLAC:0:E": "?F192:!F112,F113",
    "067PLAC:0:E": "?F29:!V123,V124",
    # Chapter G: Upper Digestive Track
    "068PLAC:0:E": "?G169:!G12,G14,G15,G20",
    "069PLAC:0:E": "?G18:!G199",
    "070PLAC:0:E": "?G459:!G42-G44,G46",
    "071PLAC:0:E": "?G54:!G559",
    "072PLAC:0:E": "?G64:!G659",
    "073PLAC:0:E": "?G79:!G809",
    "074PLAC:0:E": "?G12,G14,G16,G18,G19,G20:!G42-G46",
    "075PLAC:0:E": "?G54:!G42-G46",
    # Chapter H: Lower Digestive Track
    "076PLAC:0:E": "?H20:!H229,H23",
    "077PLAC:0:E": "?H05:!H29",
    "078PLAC:0:E": "?H21:!H24,H229",
    "079PLAC:0:E": "?H22:!H52",
    "080PLAC:0:E": "?H259:!H23,H24",
    "081PLAC:0:E": "?H25:!H229",
    "082PLAC:0:E": "?H26:!H289",
    "083PLAC:0:E": "?H27:!H289",
    "084PLAC:0:E": "?H37:!H289",
    "085PLAC:0:E": "?H38:!H23,H229",
    "086PLAC:0:E": "?H72:!H739",
    # Chapter J: Other Abdominal Organs
    "087PLAC:0:E": "?J08:!J099",
    "088PLAC:0:E": "?J09:!T43,J17",
    "089PLAC:0:E": "?J10:!J06,J11",
    "090PLAC:0:E": "?J11:!J10,J77",
    "091PLAC:0:E": "?J13:!J107",
    "092PLAC:0:E": "?J14:!J10-J13",
    "093PLAC:0:E": "?J15:!J06,J11",
    "094PLAC:0:E": "?J339:!J18",
    "095PLAC:0:E": "?J34:!J392-J394",
    "096PLAC:0:E": "?J40,J41:!J38-J39",
    "098PLAC:0:E": "?J44-J45:!J43",
    "099PLAC:0:E": "?J77:!J06,J11",
    # Chapter K: Heart
    "101PLAC:0:E": "?K10:!K04,K133,K134",
    "102PLAC:0:E": "?K11:!K04,K131,K132",
    "103PLAC:0:E": "?K12:!K04,K135,K136,K137,K138,K139",
    "104PLAC:0:E": "?K18,K19:!K04",
    "105PLAC:0:E": "?K22,K23:!K40-K52,K58",
    "106PLAC:0:E": "?K25:!K341",
    "107PLAC:0:E": "?K344:!K554",
    "108PLAC:0:E": "?K37:!K18-K19",
    "109PLAC:0:E": "?K46:!K40-K44",
    "110PLAC:0:E": "?K49,K501:!K75",
    "112PLAC:0:E": "?K554:!K344",
    "113PLAC:0:E": "?K59:!K72,X505",
    "115PLAC:0:E": "?K624:!K59",
    "116PLAC:0:E": "?K625:!K223",
    "117PLAC:0:E": "?K63:!U105,U102,U103",
    "118PLAC:0:E": "?K68:!K77",
    "119PLAC:0:E": "?K72:!K59X605",
    "120PLAC:0:E": "?K73,K74:!K59K72",
    "PCSK3:0:E": "?K75:!K49",
    "122PLAC:0:E": "?K77:!K68",
    # Chapter L: Arteries and Veins
    "123PLAC:0:E": "?L04:!L12",
    "124PLAC:0:E": "?L18:!L27,L28",
    "125PLAC:0:E": "?L27,L28:!L18,L19",
    "126PLAC:0:E": "?L56:!L48",
    "127PLAC:0:E": "?L57:!L49",
    "128PLAC:0:E": "?L58:!L50",
    "129PLAC:0:E": "?L59:!L51",
    "130PLAC:0:E": "?L73:!L776",
    "131PLAC:0:E": "?L75:!L74O05",
    "132PLAC:0:E": "?L767:!L73",
    "133PLAC:0:E": "?L773:!J114",
    "134PLAC:0:E": "?L80:!K621",
    "135PLAC:0:E": "?L85,L87:!L84",
    "136PLAC:0:E": "?L912:!L943,L997,O152,O153",
    "137PLAC:0:E": "?L93:!L19",
    "138PLAC:0:E": "?O01-O02:!O02-O03",
    "139PLAC:0:E": "?O043:!O034-O036",
    # Chapter M: Urinary
    "140PLAC:0:E": "?M062:!M136",
    "141PLAC:0:E": "?M07:!M09,M10",
    "142PLAC:0:E": "?M16:!X401",
    "143PLAC:0:E": "?M292:!M274",
    "144PLAC:0:E": "?M293:!M275",
    "145PLAC:0:E": "?M294:!M277",
    "146PLAC:0:E": "?M295:!M27",
    "147PLAC:0:E": "?M37:!M646,M542",
    "148PLAC:0:E": "?M383:!M245,M256,M247",
    "149PLAC:0:E": "?M47:!M496,U121",
    "150PLAC:0:E": "?M474:!U264,M482",
    "151PLAC:0:E": "?M496:!U127",
    "152PLAC:0:E": "?M513:!M521",
    "153PLAC:0:E": "?M583:!M564",
    "154PLAC:0:E": "?M61:!M341",
    "155PLAC:0:E": "?M676:!M707",
    # Chapter N: Male Genital Organs
    "156PLAC:0:E": "?N03:!N351",
    "157PLAC:0:E": "?N11:!T193",
    "158PLAC:0:E": "?N13:!N346",
    "159PLAC:0:E": "?N156:!N344,N345",
    "160PLAC:0:E": "?N24:!N353",
    "161PLAC:0:E": "?N32:!N352",
    "162PLAC:0:E": "?N326:!N324",
    "163PLAC:0:E": "?N34:!N35",
    # Chapter P: Lower Female Genital Tract
    "164PLAC:0:E": "?P072:!R272",
    "165PLAC:0:E": "?P24,P30:!M51,M52,M53,M54,M55",
    "166PLAC:0:E": "?P26:!Q14",
    "167PLAC:0:E": "?P273:!Q554",
    "168PLAC:0:E": "?Q052:!Q101,Q111,Q112",
    "169PLAC:0:E": "?Q053:!R152",
    "170PLAC:0:E": "?Q076:!X161",
    "171PLAC:0:E": "?Q123:!P315",
    "172PLAC:0:E": "?Q163:!Q176",
    "173PLAC:0:E": "?Q203:!R123,R30",
    "174PLAC:0:E": "?Q25:!Q27,Q28",
    "175PLAC:0:E": "?Q561:!Q41",
    "176PLAC:0:E": "?Q58:!Q091,Q11",
    # Chapter R: Female Genital Tract Associated with Pregnancy, Childbirth and Puerperium
    "177PLAC:0:E": "?R022:!R131",
    "178PLAC:0:E": "?R12:!Q20",
    "179PLAC:0:E": "?R17:!Q019",
    "180PLAC:0:E": "?R18:!Q011,R259",
    "181PLAC:0:E": "?R19,R20,R21,R22,R23,R24,R25:!Q58",
    "182PLAC:0:E": "?R27:!P13",
    "183PLAC:0:E": "?R28:!Q10,Q11",
    "184PLAC:0:E": "?R29:!R302,Q10,Q11",
    "185PLAC:0:E": "?R30:!Q09,Q20",
    "186PLAC:0:E": "?R304:!Q205",
    "187PLAC:0:E": "?R372:!R274",
    # Chapter S: Skin
    "188PLAC:0:E": "?S02:!T296",
    "189PLAC:0:E": "?S21:!C102",
    "190PLAC:0:E": "?S34:!C103",
    "191PLAC:0:E": "?S52:!X38",
    # Chapter T: Soft Tissue
    "192PLAC:0:E": "?T122:!T124",
    "193PLAC:0:E": "?T16:!G23",
    "194PLAC:0:E": "?T24:!T97",
    "195PLAC:0:E": "?T27:!T98",
    "196PLAC:0:E": "?T304:!T317",
    "197PLAC:0:E": "?T305:!J043",
    "198PLAC:0:E": "?T317:!T304",
    "199PLAC:0:E": "?T32:!T282",
    "200PLAC:0:E": "?T34:!A124,A53,L811,X402",
    "201PLAC:0:E": "?T413:!T323",
    "202PLAC:0:E": "?T415:!T323",
    "203PLAC:0:E": "?T423:!T413,T415",
    "204PLAC:0:E": "?T46:!A124,A53,L811,X402",
    "205PLAC:0:E": "?T50:!S18,S25",
    "206PLAC:0:E": "?T55:!T51",
    "207PLAC:0:E": "?T644:!W77",
    "208PLAC:0:E": "?T69:!W77",
    "209PLAC:0:E": "?T76:!S17,S24",
    "210PLAC:0:E": "?T832:!M416",
    "211PLAC:0:E": "?T97:!T244",
    # Chapter U: Diagnostic Imaging, Testing and Rehab
    "212PLAC:0:E": "?U07:!U18,U15",
    "213PLAC:0:E": "?U08:!U17",
    "214PLAC:0:E": "?U081:!U175",
    "215PLAC:0:E": "?U092:!Q555",
    "216PLAC:0:E": "?U10:!K63",
    "217PLAC:0:E": "?U11:!L00-L99",
    "218PLAC:0:E": "?U12:!U26",
    "219PLAC:0:E": "?U13:!U14",
    "220PLAC:0:E": "?U15:!U07",
    "221PLAC:0:E": "?U19:!U10",
    "222PLAC:0:E": "?U29:!U12",
    "223PLAC:0:E": "?U264:!M474",
    "224PLAC:0:E": "?U34:!U10",
    "225PLAC:0:E": "?U40:!U27",
    "226PLAC:0:E": "?U41:!U283,U341",
    "227PLAC:0:E": "?U502,U504,U505,U506:!U503",
    "228PLAC:0:E": "?U533,U534:!U531,U532",
    # Chapter V: Bones and Joins of Skull and Spine
    "229PLAC:0:E": "?V073:!F18",
    "230PLAC:0:E": "?V09:!C08",
    "231PLAC:0:E": "?V123,V124:!F03,F29",
    "232PLAC:0:E": "?V125:!V023",
    "233PLAC:0:E": "?V144:!F18",
    "234PLAC:0:E": "?V25:!V281",
    "235PLAC:0:E": "?V26:!V282",
    "236PLAC:0:E": "?V401:!V37,V38,V39",
    "237PLAC:0:E": "?V405:!V365",
    "238PLAC:0:E": "?V41:!O095",
    "239PLAC:0:E": "?V415:!V311",
    "240PLAC:0:E": "?V444:!V446",
    "241PLAC:0:E": "?V465:!V405",
    "242PLAC:0:E": "?V67:!V281",
    "243PLAC:0:E": "?V61:!V282",
    # Chapter W: Other Bones and Joints
    "244PLAC:0:E": "?W01,W02,W03,W04:!X19-X27",
    "245PLAC:0:E": "?W05:!W37-W54,W93,W98,O06,O07,)008,O18,O21,O22,O23,O24,O25,O26,O09",
    "246PLAC:0:E": "?W06:!T039",
    "247PLAC:0:E": "?W08:!W03,W04,X19-X27",
    "248PLAC:0:E": "?W086:!W06,X067-X11",
    "249PLAC:0:E": "?W12,W13:!W775,X19-X27",
    "250PLAC:0:E": "?W15:!W03,W04,X19-X27",
    "254PLAC:0:E": "?W30:!X48,X49",
    "255PLAC:0:E": "?W31:!W341",
    "256PLAC:0:E": "?W322:!W342",
    "257PLAC:0:E": "?W34:!W99",
    "258PLAC:0:E": "?W55,W56,W57,W58:!X19-X27",
    "259PLAC:0:E": "?W59:!W03,W04",
    "260PLAC:0:E": "?W65,W66,W67:!X19-X27",
    "261PLAC:0:E": "?W745:!O275",
    "262PLAC:0:E": "?W743:!O271",
    "263PLAC:0:E": "?W77,W78,W79,W81,W92:!X19-X27",
    "264PLAC:0:E": "?W962:!O371",
    "265PLAC:0:E": "?W964:!O372",
    # Chapter Y: Subsidiary Classification of Methods of Operation
    "311PLAC:0:E": "?Y52:!Y76",
    "312PLAC:0:E": "?Y53:!Y78",
    "313PLAC:0:E": "?Y532:!Y755,Y764",
    "314PLAC:0:E": "?Y536:!Y744",
    "315PLAC:0:E": "?Y671:!Y692",
    "316PLAC:0:E": "?Y68:!Y78",
    "317PLAC:0:E": "?Y681:!Y755,Y764",
    "318PLAC:0:E": "?Y766:!Y762",
    # Chapter Z: Subsidiary Classification of Sites of Operation
    "319PLAC:0:E": "?Z241:!Z226",
    "320PLAC:0:E": "?Z361:!Z95",
    "321PLAC:0:E": "?Z38:!O451,Z382",
    "322PLAC:0:E": "?Z395:!Z395,Z98",
    "323PLAC:0:E": "?Z47:!Z162,Z164,Z201,Z221,Z251",
    "324PLAC:0:E": "?Z49:!Z426,Z427,Z431,Z436,Z443,Z444",
    "325PLAC:0:E": "?Z499:!Z156",
    "326PLAC:0:E": "?Z63:!Z203",
    "327PLAC:0:E": "?O12:!Z955",
    "328PLAC:0:E": "?O33:!Z63,Z64,Z65",
    "251PLAC:0:E": "?W16:!X19-X27",
    "252PLAC:0:E": "?W19,W20,W21,W22:!W65",
    "253PLAC:0:E": "?W24,W25,W26:!W66",
    "266PLAC:0:E": "?W960:!O370",
    "267PLAC:0:E": "?W972:!O381",
    "268PLAC:0:E": "?W974:!O382",
    "269PLAC:0:E": "?W971:!O380",
    "270PLAC:0:E": "?W982:!O391",
    "271PLAC:0:E": "?W984:!O392",
    "272PLAC:0:E": "?W985:!O392",
    "273PLAC:0:E": "?W980:!O390",
    "274PLAC:0:E": "?O06,O06,O07:!W40",
    "275PLAC:0:E": "?O09:!W05",
    "276PLAC:0:E": "?O17:!W66",
    "277PLAC:0:E": "?O37:!W965,W966",
    "278PLAC:0:E": "?O38:!W975,W976",
    "279PLAC:0:E": "?O39:!W986,W987,",
    "280PLAC:0:E": "?O49:!W70,W82,W83,W89",
    "281PLAC:0:E": "?O413:!O411,O412",
    "282PLAC:0:E": "?O51:!W55",
    "283PLAC:0:E": "?X082:!X215",
    "284PLAC:0:E": "?X084:!X216",
    "285PLAC:0:E": "?X11:!X273",
    "286PLAC:0:E": "?X15:!X16",
    "287PLAC:0:E": "?X161:!Q076",
    "288PLAC:0:E": "?X28:!X29",
    "289PLAC:0:E": "?X326:!X337",
    "290PLAC:0:E": "?X353:!X441",
    "291PLAC:0:E": "?X374:!X442",
    "292PLAC:0:E": "?X385:!X443",
    "293PLAC:0:E": "?X391:!X444",
    "294PLAC:0:E": "?X44:!E952",
    "295PLAC:0:E": "?X52:!X581,E87",
    "296PLAC:0:E": "?X522:!E856",
    "297PLAC:0:E": "?X60:!X62",
    "298PLAC:0:E": "?X62:!X60",
    "299PLAC:0:E": "?X655:!X657",
    "300PLAC:0:E": "?X70,X71,X72,X73:!X74",
    "301PLAC:0:E": "?X74:!X70-X73,X81-X98",
    "302PLAC:0:E": "?X81-X98:!X74",
    "303PLAC:0:E": "?Y02:!Y14",
    "304PLAC:0:E": "?Y03:!Y15",
    "305PLAC:0:E": "?Y173:!Y176",
    "306PLAC:0:E": "?Y373:!Y352",
    "307PLAC:0:E": "?Y45:!Y53",
    "308PLAC:0:E": "?Y452:!Y743,Y753,Y765",
    "309PLAC:0:E": "?Y49:!Y74",
    "310PLAC:0:E": "?Y50:!Y75",
    # Chapter C - Eye. Exceptions are: Bilateral recession of medial recti muscles of eyes (C312),
    # Bilateral resection of medial recti muscles of eyes (C313), Bilateral recession of lateral
    # recti muscles of eyes (C314), and Bilateral resection of lateral recti muscles of eyes (C315).
    "LATCODING:0:E": "?C00-C30,C311,C316,C318,C319,C32-C99:{Z00-Z99",
    "LATCODING:1:E": "?K00-K99:>Z00-Z99",
    # U21 always requires a site code.
    "PCSU1:0:E": "?U21:{Z00-Z99",
    # Semilunar cartilage is only found in the knee joint, so is not necessary to assign a site code
    # with codes in category W82 Therapeutic endoscopic operations on semilunar cartilage
    "CSW8:0:E": "?W82:!Z00-Z99",
    # Aspiration of prosthetic joint (W901) requires a laterality
    "PCSW9:0:E": "?W901:{Z94",
    # 3D mapping of the heart is an inherent part of ablation of the conducting system of the
    # heart and is rarely performed on its own, therefore code K586 Percutaneous
    # transluminal three dimensional electroanatomic mapping of conducting system of
    # heart must not be assigned in addition to an ablation code from categories K57 Other
    # therapeutic transluminal operations on heart or K62 Therapeutic transluminal
    # operations on heart
    "PSK6:0:E": "?L586:!K57,K62",
}


def _build_standards_dict(standards_dict: dict = icd10_standards_dict) -> dict:
    compiled_standards_dict = {}
    for key, standard in standards_dict.items():
        standard = standard.split(":")

        primary_codes = hyph(standard[0][1:])

        for code in primary_codes:
            if code not in compiled_standards_dict:
                compiled_standards_dict[code] = {}

            for part in standard[1:]:
                dehyphyed = hyph(part[1:])
                if part.startswith("."):
                    if key not in compiled_standards_dict[code]:
                        compiled_standards_dict[code][key] = {}
                    compiled_standards_dict[code][key]["."] = part[1:]
                elif part[0] in ("&", "/", "^"):
                    if key not in compiled_standards_dict[code]:
                        compiled_standards_dict[code][key] = {}
                    compiled_standards_dict[code][key][part[0]] = code
                elif part[0] == "~":
                    character, have = part[1:].split("..")
                    if key not in compiled_standards_dict[code]:
                        compiled_standards_dict[code][key] = {}
                    compiled_standards_dict[code][key][part[0]] = {
                        "character": character,
                        "have": have,
                    }
                else:
                    if key not in compiled_standards_dict[code]:
                        compiled_standards_dict[code][key] = {}
                    compiled_standards_dict[code][key][part[0]] = dehyphyed
    return compiled_standards_dict
