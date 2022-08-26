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

    def test_anemia_in_leukaemia_myeloma_and_myelodysplastia(self):
        # This test validates to see whether DChS.II.2 works as intended.
        # Description: Anaemia must not be coded in leukaemia, myeloma and myelodysplasia
        # RULE : !

        # Test to see whether anaemia can be run on its own
        self.assertEqual(run(["D64"]), {})
        # Test to see whether anemia coded with leukemia returns an error
        self.assertIsNot(run(["D64", "C90"]), {"D64": {}})
        # Test to see whether unspecified anemia coded with leukemia returns an error
        self.assertIsNot(run(["D649", "C90"]), {"D649": {}})
        # Test to see whether unspecified anemia coded with unspecified leukemia returns an error
        self.assertIsNot(run(["D649", "C909"]), {"D649": {}})

    def test_mental_behavioural_exception(self):
        # This test validates to see whether DCS.XIX.8 works as intended.
        # Description: F100 should not be coded with T36-T50 - unless T510 is also assigned
        # RULE : ! and @

        # Test to see whether F100 can run on its own
        self.assertEqual(run(["F100"]), {})
        # Test to see whether F100 coded with T36 returns an error
        self.assertIsNot(run(["F100", "T36"]), {"F100": {}})
        # Test to see whether F100 coded with T36 AND T510 does not return an error
        self.assertEqual(run(["F100", "T36", "T510"]), {})

    def test_dcs_i_5(self):
        # Zika Virus must always follow Other specified mosquito-borne viral fevers
        print(run(["U068", "A928"]))

if __name__ == "__main__":
    unittest.main()
