#!/usr/bin/env python3

import os
from urllib.parse import urljoin
import requests
import json
import logging
import click
from datetime import date
import time
from scraper.parse import FantasticMovieListParser, FantasticMovieParser

BASE_URL = 'http://fantasticfest.com/films/'

REQUESTS_PER_MINUTE = 15

logger = logging.getLogger(__name__)

# Create a session in global scope
session = requests.Session()


def filename_from_title(title):
    return title.replace(' ', '-').replace('\'', '-') \
                .replace('"', '-').replace(',', '').lower()


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
            parser = FantasticMovieListParser(response.text)
            movie_urls.extend(parser.parse())
        else:
            click.secho("Request for {} failed!".format(url), fg="red")

    for n, url in enumerate(set(movie_urls)):
        click.secho("[{}] Fetching {}".format(n, url), fg="yellow")
        response = requests.request('GET', url, timeout=(1.0, 3.0))
        if response.ok:
            click.secho("[{}] Parsing {}".format(n, response.url), fg="blue")
            movie_parser = FantasticMovieParser(response.content)
            movie = movie_parser.parse()
            filename = "{}.json".format(filename_from_title(movie.title))
            if save:
                file_save_path = os.path.join(path, filename)
                click.secho("Saving {}".format(filename), fg="green")
                json.dump(movie.to_dict(), open(file_save_path, 'w'), indent=4)
            else:
                click.secho("Parsed '{}'".format(movie.title),
                            fg="green")
                click.secho(json.dumps(movie.to_dict(), indent=4),
                            fg="cyan")
        else:
            click.secho("Request for {} failed!".format(url), fg="red")
        time.sleep(0.05)
    click.secho("All done!", fg="green")


if __name__ == '__main__':
    scrape()
