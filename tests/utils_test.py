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
from codingerrors.utils import hyph


class TestHyph(unittest.TestCase):
    def test_hyph_basic(self):
        # Check to see if a single term works, in all forms.
        self.assertEqual(hyph("I10"), ["I10"])
        # X code
        self.assertEqual(hyph("I10X"), ["I10X"])
        # Five length code.
        self.assertEqual(hyph("M4792"), ["M4792"])

    def test_hyph_multiple(self):
        # Check to see if a single term works, in all forms.
        self.assertEqual(hyph("I10,J22"), ["I10", "J22"])
        self.assertEqual(hyph("I10,J22,M4792"), ["I10", "J22", "M4792"])

    def test_hyph_hyphenated(self):
        # Basic hyph down to the third character, should return three instances
        self.assertEqual(hyph("M38-M40"), ["M38", "M39", "M40"])
        # Large query over a multitude of codes over differing tens.
        self.assertEqual(len(hyph("M338-M444")), (444-338)+1)
    
    def test_spacing(self):
        # Just to see if we can deal with malformed input
        self.assertEqual(hyph("M38- M40"), ["M38", "M39", "M40"])
        self.assertEqual(hyph("M38 - M40"), ["M38", "M39", "M40"])
        self.assertEqual(hyph("M38  - M40"), ["M38", "M39", "M40"])
        self.assertEqual(hyph(" M38  - M40"), ["M38", "M39", "M40"])
        self.assertEqual(hyph(" M38  - M40   "), ["M38", "M39", "M40"])
        self.assertEqual(hyph(" M38  , M40   "), ["M38", "M40"])



if __name__ == "__main__":
    unittest.main()
