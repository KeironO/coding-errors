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


import unittest
from codingerrors import run


class TestStandards(unittest.TestCase):
    # We can't check every single standard (unrealistic, so we'll do 2 of every possible ruleset instead.)
    
    ## Tests

    # ✔️ = In check.py
    # ☑️ = Two tests written

    # &* : Can never be in the primary position ✔️
    # ^* : Must be in primary or secondary position. ✔️
    # ? : Applies to the following codes.
    # / : never code ✔️

    # ! : Cannot be coded with ☑️ ✔️
    #   - test_anemia_in_leukaemia_myeloma_and_myelodysplastia
    #   - test_mental_behavioural_exception

    # .n: Require's nth character ✔️

    # { : Must always be coded with ✔️

    # ~x..y: x character cannot be y ✔️

    # > : Should not be directly followed by ✔️

    # $ : Should always follow by ☑️ ✔️
    #   - test_zika_virus_must_alwys_follow_other_speicifed_mosquito_borne_viral_fevers
    #   - test_morbidly_adherent_placenta_following_retained_or_third_placenta
 
    # € : Should always either be sequenced directly after ✔️

    # ) : Should always be sequenced either way by  ✔️

    # ¬ : When in primary position should never be followed by  ✔️

    # @ : Exception when present (ignore) ☑️ ✔️
    #   - test_mental_behavioural_exception
    #   - test_metastatic_cancer_should_never_be_coded_with_a_hematological_cancer

    def test_anemia_in_leukaemia_myeloma_and_myelodysplastia(self):
        # This test validates to see whether DChS.II.2 works as intended.
        # Description: Anaemia must not be coded in leukaemia, myeloma and myelodysplasia
        # RULE : !

        # Test to see whether anaemia can be run on its own
        self.assertEqual(run(["D64"]), {})
        # Test to see whether anemia coded with leukemia returns an error
        self.assertIsNot(run(["D64", "C90"]), {})
        # Test to see whether unspecified anemia coded with leukemia returns an error
        self.assertIsNot(run(["D649", "C90"]), {})
        # Test to see whether unspecified anemia coded with unspecified leukemia returns an error
        self.assertIsNot(run(["D649", "C909"]), {})

    def test_mental_behavioural_exception(self):
        # This test validates to see whether DCS.XIX.8 works as intended.
        # Description: F100 should not be coded with T36-T50 - unless T510 is also assigned
        # RULE : ! and @

        # Test to see whether F100 can run on its own
        self.assertEqual(run(["F100"]), {})
        # Test to see whether F100 coded with T36 returns an error
        self.assertTrue("F100" in run(["F100", "T36"]))
        # Test to see whether F100 coded with T36 AND T510 does not return an error
        self.assertEqual(run(["F100", "T36", "T510"]), {})

    def test_zika_virus_must_alwys_follow_other_speicifed_mosquito_borne_viral_fevers(self):
        # This test validates to see whether DCS.I.5 works as intended
        # Zika Virus must always follow Other specified mosquito-borne viral fevers
        # RULE: $

        # Coded in correct position.
        self.assertEqual(run(["A928", "U068"]), {})
        # Codded in correct position with additional code prepended
        self.assertEqual(run(["J22", "A928", "U068"]), {})
        # Coded in correct position with additional code appended
        self.assertEqual(run(["J22", "A928", "U068", "I10"]), {})
        # Failed because wrong sequence.
        self.assertNotEqual(run(["J22", "U068", "A928", "I10"]), {})

    def test_morbidly_adherent_placenta_following_retained_or_third_placenta(self):
        # This test valdiates to see whether DCS.XV.19 works as intended
        # Only code O432 AFTER O720/O730
        # RULE: $

        self.assertEqual(run(["O720", "O432"]), {})
        self.assertNotEqual(run(["O432", "O720"]), {})
        self.assertEqual(run(["O720"]), {})
        # Cannot code without O720 or O730
        self.assertNotEqual(run(["O432"]), {})

    def test_metastatic_cancer_should_never_be_coded_with_a_hematological_cancer(self):
        # This test valdiates to see whether DCS.II.7 works as intended
        # C81._ to C96._ should not be coded with C77._/C78._/C79._ unless there is a code from C00-C75 or C80._ or Z85._
        # RULE: ! and @

        self.assertNotEqual(run(["C81", "C79"]), {})
        self.assertEqual(run(["C81"]), {})
        self.assertEqual(run(["C81", "C79", "Z85"]), {})






if __name__ == "__main__":
    unittest.main()
