import requests
import json
import os
from urllib.parse import urlparse

from scraper.scrape import HTMLScraper
from scraper.models import FilmDict


def get_url(url, session=None, timeout=3.0):
    if not session:
        session = requests.Session()
    return session.get(url, timeout=timeout)


def scrape_response(response, scraper_class):
    if issubclass(scraper_class, HTMLScraper):
        scraper = scraper_class(response.content, response.url)
        result = scraper.scrape()
        return result
    else:
        raise TypeError('scraper_class class must be a HTMLScraper subclass')


def filename_from_url_slug(url, basepath=None):
    url_slug = urlparse(url).path.split('/')[-1]
    filename = "{}.json".format(url_slug)
    if basepath:
        return os.path.join(os.path.abspath(basepath), filename)
    else:
        return filename


def save_scraped_film(object, filepath, indent=4):
    if isinstance(object, FilmDict):
        try:
            with open(filepath, 'w') as fp:
                json.dump(object.data, fp, ensure_ascii=False, sort_keys=True, indent=indent)
        except TypeError as e:
            raise e
        except Exception as e:
            raise e
    else:
        raise TypeError('Film object must be an instance of FilmDict')


def film_to_json_string(object, indent=4):
    if isinstance(object, FilmDict):
        return json.dumps(object.data, ensure_ascii=False, sort_keys=True, indent=indent)
    else:
        raise TypeError('Film object must be an instance of FilmDict')
