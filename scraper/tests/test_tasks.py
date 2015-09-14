import unittest

from scraper.tasks import *


class TestScraperTasks(unittest.TestCase):

    def test_get_url_session(self):
        '''get_url works with a passed session object'''
        self.fail("Test stub needs implementation")

    def test_generic_scrape_response(self):
        '''scrape_response... in its scraper TestCases'''
        pass

    def test_filename_from_url_slug(self):
        '''filename_from_url_slug makes the expected filename from a url with a slug'''
        self.fail("Test stub needs implementation")

    def test_save_scraped_film(self):
        '''save_scraped_film dumps a FilmDict to a file pointer without error'''
        self.fail("Test stub needs implementation")

    def test_save_scraped_film_sorted(self):
        '''save_scraped_film sorts keys on serialization'''
        self.fail("Test stub needs implementation")

    def test_save_scraped_film_fails(self):
        '''save_scraped_film raises an error on non-FilmDict object'''
        self.fail("Test stub needs implementation")

    def test_film_to_json_string(self):
        '''film_to_json_string can serialized a FilmDict object to string'''
        self.fail("Test stub needs implementation")

    def test_film_to_json_string_sorted(self):
        '''film_to_json_string sorts keys on serialization'''
        self.fail("Test stub needs implementation")

    def test_film_to_json_string_fails(self):
        '''film_to_json_string raises an error on a non-FilmDict object'''
        self.fail("Test stub needs implementation")


