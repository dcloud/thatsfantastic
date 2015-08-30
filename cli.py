#!/usr/bin/env python3

import os
from urllib.parse import urljoin, urlparse
import requests
import json
import logging
import click
import time
from scraper.scrape import FantasticMovieListScraper, FantasticMovieScraper

BASE_URL = 'http://fantasticfest.com/films/'

REQUESTS_PER_MINUTE = 15

logger = logging.getLogger(__name__)

# Create a session in global scope
session = requests.Session()


@click.command()
@click.argument('path', type=click.Path(exists=True, file_okay=False, writable=True))
@click.option('--festival-url', type=str, default=BASE_URL)
@click.option('--offset', default=18)
@click.option('--max-pages', type=click.IntRange(min=1, clamp=True), default=1)
@click.option('--save/--no-save', default=False)
def scrape(path, festival_url, offset, max_pages, save):
    'Scrape films from the Fantastic Fest website'

    if festival_url[-1] != '/':
        festival_url += '/'

    click.secho("Fest URL {}".format(festival_url), fg="yellow")

    session.save_path = os.path.abspath(path)

    page_offsets = range(0, offset * max_pages, offset)
    page_urls = [urljoin(festival_url, "P{0:d}".format(offset)) for offset in page_offsets]
    movie_urls = []
    for url in page_urls:
        click.secho("Fetching {}".format(url), fg="yellow")
        response = session.get(url)
        if response.ok:
            click.secho("Parsing {}".format(response.url), fg="blue")
            list_scraper = FantasticMovieListScraper(response.text)
            movie_urls.extend(list_scraper.scrape())
        else:
            click.secho("Request for {} failed!".format(url), fg="red")

    for n, url in enumerate(set(movie_urls)):
        start_time = time.time()
        click.secho("[{}] Fetching {}".format(n, url), fg="yellow")
        response = requests.request('GET', url, timeout=(1.0, 3.0))
        if response.ok:
            click.secho("[{}] Parsing {}".format(n, response.url), fg="blue")
            movie_scraper = FantasticMovieScraper(response.content)
            movie = movie_scraper.scrape()
            filmpath = urlparse(response.url).path.split('/')[-1]
            filename = "{}.json".format(filmpath)
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
        time_delay = 0.05
        sleep_time = time_delay - (time.time() - start_time)
        if sleep_time > 0:
            time.sleep(sleep_time)
    click.secho("All done!", fg="green")


if __name__ == '__main__':
    scrape()
