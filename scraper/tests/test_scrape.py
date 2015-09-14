import unittest

from scraper.scrape import (HTMLScraper, FantasticMovieScraper, FantasticMovieListScraper)
from scraper.models import FilmDict


class TestHTMLScraper(unittest.TestCase):
    """Tests the HTMLScraper"""

    def test_make_lxml_tree_raw_html(self):
        '''HTMLScraper creates an lxml tree for raw_html'''
        self.fail("Test stub needs implementation")

    def test_source_url(self):
        '''HTMLScraper can store a source_url'''
        self.fail("Test stub needs implementation")


class TestFantasticMovieScraper(unittest.TestCase):
    """Tests the FantasticMovieScraper"""

    def test_raw_metadata(self):
        '''raw_metadata runs scrape for all FilmDict.attributes'''
        self.fail("Test stub needs implementation")

    def test_raw_title(self):
        '''raw_title gets a raw title'''
        self.fail("Test stub needs implementation")

    def test_raw_description(self):
        '''raw_description gets a raw description'''
        self.fail("Test stub needs implementation")

    def test_raw_synopsis(self):
        '''raw_synopsis gets a raw synopsis'''
        self.fail("Test stub needs implementation")

    def test_raw_directors(self):
        '''raw_directors gets a raw directors string'''
        self.fail("Test stub needs implementation")

    def test_raw_countries(self):
        '''raw_countries gets a raw countries list'''
        self.fail("Test stub needs implementation")

    def test_raw_year(self):
        '''raw_year gets a raw year'''
        self.fail("Test stub needs implementation")

    def test_raw_runtime(self):
        '''raw_runtime gets a raw runtime'''
        self.fail("Test stub needs implementation")

    def test_clean_title(self):
        '''clean_title can create a properly cleaned title for a film'''
        self.fail("Test stub needs implementation")

    def test_clean_description(self):
        '''clean_description can create a properly cleaned description for a film'''
        self.fail("Test stub needs implementation")

    def test_clean_synopsis(self):
        '''clean_synopsis can create a properly cleaned synopsis for a film'''
        self.fail("Test stub needs implementation")

    def test_clean_directors(self):
        '''clean_directors can create a properly cleaned directors for a film'''
        self.fail("Test stub needs implementation")

    def test_clean_countries(self):
        '''clean_countries can create a properly cleaned countries for a film'''
        self.fail("Test stub needs implementation")

    def test_clean_year(self):
        '''clean_year can create a properly cleaned year for a film'''
        self.fail("Test stub needs implementation")

    def test_clean_runtime(self):
        '''clean_runtime can create a properly cleaned runtime for a film'''
        self.fail("Test stub needs implementation")


class TestFantasticMovieListScraper(unittest.TestCase):
    """Tests the FantasticMovieListScraper"""

    def test_get_film_page_urls(self):
        '''get_film_page_urls gets urls to film description pages'''
        self.fail("Test stub needs implementation")
