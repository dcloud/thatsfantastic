import unittest

from scraper.utils import (correct_web_url, is_web_url, unicode_normalize,
                           deeducate_quotes, clean_string, string_to_list)


class TestURLUtils(unittest.TestCase):
    """Tests correct_web_url, is_web_url utils"""

    def setUp(self):
        self.valid_url = 'http://fantasticfest.com/films'
        self.no_scheme_url = 'www.fantasticfest.com/films'
        self.not_web_url = 'ssh://server.com/path/to/things/'

    def test_correct_no_scheme_url(self):
        '''correct_web_url prepends a scheme when not provided'''
        corrected_url = correct_web_url(self.no_scheme_url)

        self.assertEqual(corrected_url, 'https://www.fantasticfest.com/films')

    def test_correct_append_slash(self):
        '''correct_web_url appends a slash when append_slash is True'''
        corrected_url = correct_web_url(self.no_scheme_url, append_slash=True)

        self.assertEqual(corrected_url, 'https://www.fantasticfest.com/films/')

    def test_is_not_web_url(self):
        '''is_web_url correctly identifies a non-http URL'''
        self.assertFalse(is_web_url(self.not_web_url))

    def test_is_web_url(self):
        '''is_web_url correctly identifies a valid URL'''
        self.assertTrue(is_web_url(self.valid_url))


class TestStringUtils(unittest.TestCase):
    """Tests string utils"""
    def setUp(self):
        self.has_decomposed_unicode_str = "N\u006F\u0308e"

    def test_compose_unicode_normalize(self):
        '''unicode_normalize composes a single unicode character from a decomposed pair'''
        result = unicode_normalize(self.has_decomposed_unicode_str)
        self.assertEqual(result, "Nöe")

    def test_deeducation_of_quotes(self):
        '''deeducate_quotes takes "fancy" quotes and turns them into dull ones.'''
        self.fail("Test stub needs implementation")

    def test_clean_string(self):
        '''clean_string runs deeducate_quotes, and gets rid of whitespace.'''
        self.fail("Test stub needs implementation")

    def test_string_to_list(self):
        '''string_to_list splits a comma-separarated string into a list,
        then deeducates quotes and gets rid of whitespace.'''
        self.fail("Test stub needs implementation")


class TestHTMLUtils(unittest.TestCase):
    """Test HTML Urils"""

    # def setUp(self):
    #     self.unicode_html = "N\u006F\u0308e"

    def test_decode_html(self):
        '''decode_html converts an html string into unicode html.'''
        self.fail("Test stub needs implementation")
