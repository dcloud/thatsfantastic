import json
import os
from urllib.parse import urlparse
import requests
from cachecontrol import CacheControl
from cachecontrol.caches import FileCache
from django.conf import settings

from scraper.scrape import HTMLScraper
from scraper.models import FilmDict

default_cache = FileCache(".webcache")

SCRAPER_USER_AGENT = getattr(settings, "SCRAPER_USER_AGENT", "Fantastic Movie Scraper")


def make_session(cache=default_cache):
    session = requests.Session()
    session.headers.update({"User-Agent": SCRAPER_USER_AGENT})
    if cache:
        session = CacheControl(session, cache=cache)
    return session


def get_url(url, session=None, timeout=3.0, cache=default_cache):
    if not session:
        session = make_session(cache=cache)
    return session.get(url, timeout=timeout)


def scrape_response(response, scraper_class):
    if issubclass(scraper_class, HTMLScraper):
        scraper = scraper_class(response.content, response.url)
        result = scraper.scrape()
        return result
    else:
        raise TypeError("scraper_class class must be a HTMLScraper subclass")


def filename_from_url_path(url, basepath=None, fileext="json"):
    url_slug = urlparse(url).path.rstrip("/").split("/")[-1]
    filename = "{0}.{1}".format(url_slug, fileext)
    if basepath:
        return os.path.join(os.path.abspath(basepath), filename)
    else:
        return filename


def save_scraped_film(object, filepath, indent=4):
    if isinstance(object, FilmDict):
        try:
            with open(filepath, "w") as fp:
                json.dump(
                    object.data, fp, ensure_ascii=False, sort_keys=True, indent=indent
                )
        except TypeError as e:
            raise e
        except Exception as e:
            raise e
    else:
        raise TypeError("Film object must be an instance of FilmDict")


def film_to_json_string(object, indent=4):
    if isinstance(object, FilmDict):
        return json.dumps(
            object.data, ensure_ascii=False, sort_keys=True, indent=indent
        )
    else:
        raise TypeError("Film object must be an instance of FilmDict")
