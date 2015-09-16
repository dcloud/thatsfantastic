import unittest
import requests
import cachecontrol
import betamax
import os
import json

from scraper.tasks import *
from scraper.scrape import (HTMLScraper,)
from scraper.tests import (CASSETTES_DIR,)

BASE_TEST_URL = "http://httpbin.org/"


class TestScraperTasks(unittest.TestCase):

    def test_make_session(self):
        '''make_session makes a file-cached session by default'''
        sess = make_session()
        self.assertIsInstance(sess, requests.Session)
        self.assertEqual(sess.headers.get('User-Agent'), SCRAPER_USER_AGENT)
        for key, adapter in sess.adapters.items():
            self.assertTrue(hasattr(adapter, "cache"))
            self.assertIsInstance(adapter.cache, cachecontrol.caches.FileCache)

    def test_make_session_uncached(self):
        '''make_session can make a session that is not under cachecontrol'''
        sess = make_session(cache=None)
        self.assertIsInstance(sess, requests.Session)
        for key, adapter in sess.adapters.items():
            self.assertNotIsInstance(adapter, cachecontrol.adapter.CacheControlAdapter)

    def test_get_url_session(self):
        '''get_url works with a passed session object'''
        sess = requests.Session()
        recorder = betamax.Betamax(sess, cassette_library_dir=CASSETTES_DIR)
        with recorder.use_cassette('test_get_url_session'):
            resp = get_url(BASE_TEST_URL, session=sess)
            self.assertIsNotNone(resp)
            self.assertTrue(resp.ok)
            self.assertNotEqual(resp.request.headers.get('User-Agent'), SCRAPER_USER_AGENT)

    def test_generic_scrape_raises_error(self):
        '''scrape_response raises a NotImplementedError when passed HTMLScraper'''
        resp = get_url(BASE_TEST_URL)
        self.assertIsNotNone(resp)
        with self.assertRaises(NotImplementedError):
            scrape_response(resp, HTMLScraper)

    def test_filename_from_url_path(self):
        '''filename_from_url_path makes the expected filename from a url with a path'''
        url = 'http://thatsfantastic.herokuapp.com/films/alike-different/#foo?q=bah&t=r'
        filename = filename_from_url_path(url)
        self.assertEqual(filename, 'alike-different.json')

    def test_save_scraped_film_requires_filmdict(self):
        '''save_scraped_film dumps a FilmDict to a file pointer without error'''
        with self.assertRaises(TypeError):
            save_scraped_film({'title': 'The Fake'}, '/tmp/test_save_scrape')

    def test_save_scraped_film_sorted(self):
        '''save_scraped_film sorts keys on serialization'''
        fpath = '/tmp/test_save_scrape'
        if os.path.exists(fpath):
            self.fail("File exists at test path '{}'".format(fpath))
        object = FilmDict(initialdata={'title': 'The Fake', 'description': 'foo'})
        save_scraped_film(object, fpath)
        self.assertTrue(os.path.exists(fpath))
        with open(fpath, 'r') as fp:
            contents = fp.read()
            d_pos = contents.find('description')
            t_pos = contents.find('title')
            self.assertLess(d_pos, t_pos)
            self.assertIn("    ", contents)
        os.remove(fpath)

    def test_film_to_json_string(self):
        '''film_to_json_string can serialized a FilmDict object to a json string, with sorted keys'''
        object = FilmDict(initialdata={'title': 'The Fake', 'description': 'foo'})
        json_string = film_to_json_string(object)
        self.assertNotEqual(json_string, "")
        d_pos = json_string.find('description')
        t_pos = json_string.find('title')
        self.assertLess(d_pos, t_pos)
        self.assertIn("    ", json_string)

    def test_film_to_json_string_fails(self):
        '''film_to_json_string raises an error on a non-FilmDict object'''
        with self.assertRaises(TypeError):
            film_to_json_string({'title': 'The Fake'})
