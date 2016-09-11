from django.core.management.base import BaseCommand, CommandError
from django.utils.termcolors import make_style
from urllib.parse import urljoin
import requests
from scraper.scrape import FantasticMovieListScraper
from scraper.tasks import (get_url, scrape_response)
from scraper.utils import correct_web_url


class Command(BaseCommand):
    """Scrape a Fantastic Fest Movie list page for links to detail pages."""

    BASE_URL = 'http://fantasticfest.com/films/'

    def _setup_styles(self, no_color=False):
        if no_color or not self.stdout.isatty():
            self.info_style = self.data_style = lambda x: x
        else:
            self.info_style = make_style(fg='yellow')
            self.data_style = make_style(fg='cyan')

    def _stdout_info(self, string):
        self.stdout.write(self.info_style(string))

    def _stdout_data(self, string):
        self.stdout.write(self.data_style(string))

    def add_arguments(self, parser):
        parser.add_argument('--url', help="A URL to a Fantastic Fest movie list section.\
                                           Default: %(default)s",
                            default=Command.BASE_URL)
        parser.add_argument('--timeout', nargs='?', type=float, default=3.0,
                            help='Number of seconds to wait for a request to complete before giving up. Default: %(default)s')
        parser.add_argument('--page-size', type=int, default=18,
                            help='Number of films to per page. Used to calculate offset for next page. Default: %(default)s')
        parser.add_argument('--start-page', type=int, default=0,
                            help='0-indexed page to start scraping from. Default: %(default)s')
        parser.add_argument('--max-pages', type=int, default=1,
                            help='Maximum number of pages to fetch. Default: %(default)s')

    def handle(self, *args, **options):
        self._setup_styles(no_color=options.get('no_color', False))
        self.verbosity = options['verbosity']
        self.page_size = options['page_size']
        self.start_page = options['start_page']
        self.max_pages = options['max_pages']

        try:
            self.url = correct_web_url(options['url'], http_scheme='http')
        except TypeError as e:
            raise CommandError(e)

        if self.url[-1] != '/':
            self.url += '/'
        self.session = requests.Session()

        page_page_sizes = range(self.start_page * self.page_size, self.page_size * self.max_pages, self.page_size)
        page_urls = [urljoin(self.url, "P{0:d}".format(p_off)) for p_off in page_page_sizes]

        movie_urls = []
        for p_url in page_urls:
            movie_urls.extend(self._collect_links_for_page(p_url))

        for url in movie_urls:
            self._stdout_data(url)

    def _collect_links_for_page(self, url):
        response = get_url(url, session=self.session)
        if response.ok:
            if self.verbosity > 1:
                self._stdout_info("Parsing {}".format(response.url))
            return scrape_response(response, FantasticMovieListScraper)
        else:
            self.stderr.write("Request for {} failed. Reason: {}".format(url, response.reason))
