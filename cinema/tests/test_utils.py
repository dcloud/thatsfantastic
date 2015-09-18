import unittest

from cinema.utils import titlecase


class TestTitlecaseUtil(unittest.TestCase):
    """Test the homemade titlecase function made for titlecasing movies"""

    def test_titlecase_with_apostrophes(self):
        '''titlecase should not captialize a letter that immediately follows an apostrophe'''
        raw_title = "THE MILL AT CALDER'S END"
        corrected_title = titlecase(raw_title)
        self.assertEqual(corrected_title,
                         "The Mill At Calder's End")

    def test_titlecase_smallwords(self):
        '''titlecase lowercase a set of 'small words' '''
        raw_title = "THE ONE WITH A HAT AND AN ALIBI BY EL HOMBRE DE COCINA VS UN BAD SPANISH"
        corrected_title = titlecase(raw_title)
        self.assertEqual(corrected_title,
                         "The One with a Hat and an Alibi by el Hombre de Cocina vs un Bad Spanish")

    def test_titlecase_with_periods(self):
        '''titlecase should captialize a letter that immediately follows a period, as in a name's initials'''
        raw_title = "THE GLORIOUS WORKS OF G.F. ZWAEN"
        corrected_title = titlecase(raw_title)
        self.assertEqual(corrected_title,
                         "The Glorious Works of G.F. Zwaen")

    def test_titlecase_with_hyphens(self):
        '''titlecase should captialize a letter that immediately follows a hyphen'''
        raw_title = "CHRONIC-CON Episode 420: A New Dope"
        corrected_title = titlecase(raw_title)
        self.assertEqual(corrected_title,
                         "Chronic-Con Episode 420: A New Dope")

    def test_titlecase_with_spaceless_plus(self):
        '''titlecase should captialize a letter that immediately follows a + sign'''
        raw_title = "VIC+FLO SAW A BEAR"
        corrected_title = titlecase(raw_title)
        self.assertEqual(corrected_title,
                         "Vic+Flo Saw a Bear")

    def test_titlecase_with_alphanumbers(self):
        '''titlecase should captialize a letter that immediately follows a + sign'''
        raw_title = "2001AD THE 1ST, 2ND, 3RD, 4TH WITH R2-D2 AND SK1 IN 3D AND 2D"
        corrected_title = titlecase(raw_title)
        self.assertEqual(corrected_title,
                         "2001AD the 1st, 2nd, 3rd, 4th with R2-D2 and SK1 in 3D and 2D")
