import unittest
import betamax

from scraper.scrape import (HTMLScraper, FantasticMovieScraper, FantasticMovieListScraper)
from scraper.models import FilmDict
from scraper.tasks import (get_url, make_session)
from scraper.tests import (CASSETTES_DIR,)

import lxml.html


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

    def setUp(self):
        self.many_directors_url = "http://fantasticfest.com/films/abcs-of-death-2"
        self.many_directors_title = "ABCs of Death 2"
        self.many_directors_sample_directors = ["Larry Fessenden", "Juan Martínez Moreno"]
        self.many_countries_url = "http://fantasticfest.com/films/the-strange-colour-of-your-bodys-tears"
        self.many_countries_countries = ["France", "Belgium", "Luxembourg"]
        self.many_countries_year = 2013
        self.many_countries_runtime = 102
        self.session = make_session()
        self.recorder = betamax.Betamax(self.session, cassette_library_dir=CASSETTES_DIR)

    def test_scraper_tree(self):
        '''scraper.tree is an instance of lxml.html.HTMLElement'''
        with self.recorder.use_cassette('many_directors'):
            resp = get_url(self.many_directors_url, session=self.session)
            scraper = FantasticMovieScraper(resp.content)
            self.assertIsInstance(scraper.tree, lxml.html.HtmlElement)

    def test_scraper_scrape(self):
        '''scraper.scrape() returns a FilmDictObject'''
        with self.recorder.use_cassette('many_directors'):
            resp = get_url(self.many_directors_url, session=self.session)
            scraper = FantasticMovieScraper(resp.content)
            film = scraper.scrape()
            self.assertIsInstance(film, FilmDict)

    def test_raw_metadata(self):
        '''raw_metadata runs scrape for all FilmDict.attributes'''
        with self.recorder.use_cassette('many_directors'):
            resp = get_url(self.many_directors_url, session=self.session)
            scraper = FantasticMovieScraper(resp.content)
            scraper.scrape()
            self.assertEqual(scraper.raw_metadata, scraper._raw_metadata)
            self.assertIsNotNone(scraper.raw_metadata)
            self.assertIsInstance(scraper.raw_metadata, (str, bytes))
            self.assertIn(",", scraper.raw_metadata)
            self.assertNotIn("<", scraper.raw_metadata)

    def test_raw_title(self):
        '''raw_title gets a raw title'''
        with self.recorder.use_cassette('many_directors'):
            resp = get_url(self.many_directors_url, session=self.session)
            scraper = FantasticMovieScraper(resp.content)
            scraper.scrape()
            self.assertIn(self.many_directors_title, scraper.raw_title)

    def test_raw_description(self):
        '''raw_description gets a raw description'''
        with self.recorder.use_cassette('many_directors'):
            resp = get_url(self.many_directors_url, session=self.session)
            scraper = FantasticMovieScraper(resp.content)
            scraper.scrape()
            self.assertNotEqual(scraper.raw_description, "")
            self.assertNotIn("\n\n\n", scraper.raw_description)

    def test_raw_synopsis(self):
        '''raw_synopsis gets a raw synopsis'''
        with self.recorder.use_cassette('many_directors'):
            resp = get_url(self.many_directors_url, session=self.session)
            scraper = FantasticMovieScraper(resp.content)
            scraper.scrape()
            self.assertNotEqual(scraper.raw_synopsis, "")
            self.assertGreater(len(scraper.raw_synopsis), 1)
            self.assertNotIn("\n\n\n", scraper.raw_synopsis)

    def test_raw_directors(self):
        '''raw_directors gets a raw directors string'''
        with self.recorder.use_cassette('many_directors'):
            resp = get_url(self.many_directors_url, session=self.session)
            scraper = FantasticMovieScraper(resp.content)
            scraper.scrape()
            self.assertNotEqual(scraper.raw_directors, "")
            self.assertIn(",", scraper.raw_directors)
            for item in self.many_directors_sample_directors:
                self.assertIn(item.lower(), scraper.raw_directors.lower())

    def test_raw_countries(self):
        '''raw_countries gets a raw countries list'''
        with self.recorder.use_cassette('many_countries'):
            resp = get_url(self.many_countries_url, session=self.session)
            scraper = FantasticMovieScraper(resp.content)
            scraper.scrape()
            self.assertIsInstance(scraper.raw_countries, list)
            self.assertNotEqual(scraper.raw_countries, [])
            for item in self.many_countries_countries:
                self.assertIn(item.upper(), (x.upper() for x in scraper.raw_countries))

    def test_raw_year(self):
        '''raw_year gets a raw year'''
        with self.recorder.use_cassette('many_countries'):
            resp = get_url(self.many_countries_url, session=self.session)
            scraper = FantasticMovieScraper(resp.content)
            scraper.scrape()
            self.assertEqual(str(self.many_countries_year), scraper.raw_year)

    def test_raw_runtime(self):
        '''raw_runtime gets a raw runtime'''
        with self.recorder.use_cassette('many_countries'):
            resp = get_url(self.many_countries_url, session=self.session)
            scraper = FantasticMovieScraper(resp.content)
            scraper.scrape()
            self.assertEqual(str(self.many_countries_runtime), scraper.raw_runtime)

    def test_clean_title(self):
        '''clean_title can create a properly cleaned title for a film'''
        with self.recorder.use_cassette('many_directors'):
            resp = get_url(self.many_directors_url, session=self.session)
            scraper = FantasticMovieScraper(resp.content)
            scraper.scrape()
            self.assertEqual(scraper.clean_title(), "ABCs of Death 2")

    def test_clean_description(self):
        '''clean_description can create a properly cleaned description for a film'''
        with self.recorder.use_cassette('many_countries'):
            resp = get_url(self.many_countries_url, session=self.session)
            scraper = FantasticMovieScraper(resp.content)
            scraper.scrape()
            self.assertNotEqual(scraper.clean_description, "")
            self.assertIn("one of the most unique experiences you have at Fantastic Fest this year.",
                          scraper.clean_description())

    def test_clean_synopsis(self):
        '''clean_synopsis can create a properly cleaned synopsis for a film'''
        with self.recorder.use_cassette('many_directors'):
            resp = get_url(self.many_directors_url, session=self.session)
            scraper = FantasticMovieScraper(resp.content)
            scraper.scrape()
            self.assertNotEqual(scraper.clean_synopsis(), "")
            self.assertIn("Twenty-six NEW ways to die.", scraper.clean_synopsis())

    def test_clean_directors(self):
        '''clean_directors can create a properly cleaned directors for a film'''
        with self.recorder.use_cassette('many_directors'):
            resp = get_url(self.many_directors_url, session=self.session)
            scraper = FantasticMovieScraper(resp.content)
            scraper.scrape()
            self.assertIsInstance(scraper.clean_directors(), list)
            for item in self.many_directors_sample_directors:
                self.assertIn(item, scraper.clean_directors())

    def test_clean_countries(self):
        '''clean_countries can create a properly cleaned countries for a film'''
        with self.recorder.use_cassette('many_countries'):
            resp = get_url(self.many_countries_url, session=self.session)
            scraper = FantasticMovieScraper(resp.content)
            scraper.scrape()
            self.assertIsInstance(scraper.clean_countries(), list)
            self.assertEqual(scraper.clean_countries(), self.many_countries_countries)

    def test_clean_year(self):
        '''clean_year can create a properly cleaned year for a film'''
        with self.recorder.use_cassette('many_countries'):
            resp = get_url(self.many_countries_url, session=self.session)
            scraper = FantasticMovieScraper(resp.content)
            scraper.scrape()
            self.assertIsInstance(scraper.clean_year(), int)
            self.assertEqual(scraper.clean_year(), self.many_countries_year)

    def test_clean_runtime(self):
        '''clean_runtime can create a properly cleaned runtime for a film'''
        with self.recorder.use_cassette('many_countries'):
            resp = get_url(self.many_countries_url, session=self.session)
            scraper = FantasticMovieScraper(resp.content)
            scraper.scrape()
            self.assertIsInstance(scraper.clean_runtime(), int)
            self.assertEqual(scraper.clean_runtime(), self.many_countries_runtime)


class TestFantasticMovieListScraper(unittest.TestCase):
    """Tests the FantasticMovieListScraper"""

    def test_get_film_page_urls(self):
        '''get_film_page_urls gets urls to film description pages'''
        self.fail("Test stub needs implementation")
