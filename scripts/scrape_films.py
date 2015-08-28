#!/usr/bin/env python3

from bs4 import UnicodeDammit
import unicodedata
import lxml.html
from lxml.cssselect import CSSSelector
import os
from urllib.parse import urljoin
import requests
import json
import re
import logging
import click
from datetime import date
import time

BASE_URL = 'http://fantasticfest.com/films/'

DEFAULT_EXCLUDE_CLASSES = set(['shareBox', 'alert', 'carousel', 'carousel-inner'])

REQUESTS_PER_MINUTE = 15

META_REGEX = r'(?P<year>\d{4}),\s+DIR\.\s+(?P<directors>(?:[\w\s\.]+\,*)+),\s+(?P<runtime>\d+)\s+MIN\.,\s+(?P<country>[\w\s]+)'

meta_searcher = re.compile(META_REGEX, flags=re.I)

logger = logging.getLogger(__name__)

META_SELECTOR = CSSSelector('header.carousel-caption > h6')
ANCHOR_SELECTOR = CSSSelector('ul.thumbnails > li .thumbnail > a:nth-of-type(1)')
BODY_TEXT_SELECTOR = CSSSelector('article h4 + p')
SYNOPSIS_SELECTOR = CSSSelector('.lead p')

CHAR_REPLACEMENT_MAP = {
    '\u2018': '\u0027',
    '\u2019': '\u0027',
    '\u201C': '\u0022',
    '\u201D': '\u0022',
}


def deeducate_quotes(string):
    for k, v in CHAR_REPLACEMENT_MAP.items():
        string = string.replace(k, v)
    return string


def decode_html(html_string):
    converted = UnicodeDammit(html_string, is_html=True)
    if not converted.unicode_markup:
        raise UnicodeDecodeError(
            "Failed to detect encoding, tried [%s]",
            ', '.join(converted.triedEncodings))
    normalized_markup = unicodedata.normalize('NFKC', converted.unicode_markup)
    return normalized_markup


def tree_from_html(html_string):
    decoded_html = decode_html(html_string)
    return lxml.html.fromstring(decoded_html)


def get_meta_info(root):
    meta_el = META_SELECTOR(root)[0]
    meta_text = deeducate_quotes(meta_el.text)
    match = meta_searcher.search(meta_text)
    if match:
        return match.groupdict()
    return None


def get_film_page_urls(root):
    anchor_list = ANCHOR_SELECTOR(root)
    return (a.attrib.get('href', None) for a in anchor_list)


def extract_body_text(root):
    body_elements = BODY_TEXT_SELECTOR(root)
    return body_elements[0].text_content() if len(body_elements) > 0 else None


def extract_synopsis(root):
    body_elements = SYNOPSIS_SELECTOR(root)
    return body_elements[0].text_content() if len(body_elements) > 0 else None


def extract_title(root):
    raw_title = root.find('*/title').text
    return raw_title.strip(' | Fantastic Fest').title()


def clean_text(text):
    text = text.strip()
    return deeducate_quotes(text)


def parse_film_information(response):
    root = tree_from_html(response.text)
    film_title = extract_title(root)
    raw_body = extract_body_text(root)
    raw_synopsis = extract_synopsis(root)
    meta_info = get_meta_info(root)
    film_info = {
        'title': clean_text(film_title),
        'raw_body': clean_text(raw_body),
        'raw_synopsis': clean_text(raw_synopsis),
    }
    if meta_info:
        film_info['year'] = int(meta_info['year'])
        film_info['directors'] = [x.strip().title() for x in meta_info.get('directors', '').split(',')]
        film_info['runtime'] = int(meta_info.get('runtime', None))
        film_info['country'] = meta_info.get('country', '').title()
    return film_info

# Create a session in global scope
session = requests.Session()


@click.command()
@click.argument('path', type=click.Path(exists=True, file_okay=False, writable=True))
@click.option('--year', default=date.today().year)
@click.option('--offset', default=18)
@click.option('--max-pages', type=click.IntRange(min=1, clamp=True), default=1)
@click.option('--save/--no-save', default=False)
def scrape(path, year, offset, max_pages, save):
    'Scrape films from the Fantastic Fest website'

    session.save_path = os.path.abspath(path)

    page_offsets = range(0, offset * max_pages, offset)
    page_urls = [urljoin(BASE_URL, "P{0:d}".format(offset)) for offset in page_offsets]
    movie_urls = []
    for url in page_urls:
        click.secho("Fetching {}".format(url), fg="yellow")
        response = session.get(url)
        if response.ok:
            click.secho("Parsing {}".format(response.url), fg="blue")
            root = tree_from_html(response.text)
            movie_urls += get_film_page_urls(root)
        else:
            click.secho("Request for {} failed!".format(url), fg="red")

    for n, url in enumerate(set(movie_urls)):
        click.secho("[{}] Fetching {}".format(n, url), fg="yellow")
        response = requests.get(url)
        if response.ok:
            click.secho("[{}] Parsing {}".format(n, response.url), fg="blue")
            film_info = parse_film_information(response)
            url_end = os.path.split(response.url)[-1]
            filename = "{}.json".format(url_end)
            if save:
                file_save_path = os.path.join(path, filename)
                click.secho("Saving {}".format(filename), fg="green")
                json.dump(film_info, open(file_save_path, 'w'), indent=4)
            else:
                click.secho("Parsed '{}'".format(film_info.get('title', 'Unknown title')),
                            fg="green")
                click.secho(json.dumps(film_info, indent=4),
                            fg="cyan")
        else:
            click.secho("Request for {} failed!".format(url), fg="red")
        time.sleep(0.10)



if __name__ == '__main__':
    scrape()
