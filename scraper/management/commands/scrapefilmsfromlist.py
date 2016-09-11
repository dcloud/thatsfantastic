from django.core.management.base import BaseCommand, CommandError
from django.utils.termcolors import make_style
from django.core import management
import io
import os
from scraper.management.commands import scrapefilmlist


class Command(BaseCommand):
    """Scrapes films from Fantastic Fest film list pages."""

    def _setup_styles(self, no_color=False):
        if no_color or not self.stdout.isatty():
            self.info_style = self.data_style = lambda x: x
        else:
            self.info_style = make_style(fg='yellow')
            self.data_style = make_style(fg='blue')

    def _stdout_info(self, string):
        self.stdout.write(self.info_style(string))

    def _stdout_data(self, string):
        self.stdout.write(self.data_style(string))

    def add_arguments(self, parser):
        parser.add_argument('--url', help="A URL to a Fantastic Fest movie list section.\
                                           Default: %(default)s",
                            default=scrapefilmlist.Command.BASE_URL)
        parser.add_argument('--timeout', nargs='?', type=float, default=3.0,
                            help='Number of seconds to wait for a request to complete before giving up. Default: %(default)s')
        parser.add_argument('--page-size', type=int, default=18,
                            help='Number of films to per page. Used to calculate offset for next page. Default: %(default)s')
        parser.add_argument('--start-page', type=int, default=0,
                            help='0-indexed page to start scraping from. Default: %(default)s')
        parser.add_argument('--max-pages', type=int, default=1,
                            help='Maximum number of pages to fetch. Default: %(default)s')
        parser.add_argument('--savepath', nargs='?',
                            help='Provide a path to a directory to save the files to.')

    def handle(self, *args, **options):
        self._setup_styles()
        self.verbosity = options['verbosity']
        self.url = options['url']
        self.page_size = options['page_size']
        self.start_page = options['start_page']
        self.max_pages = options['max_pages']
        if self.url[-1] != '/':
            self.url += '/'
        self.savepath = options.get('savepath', None)
        if self.savepath and not os.path.isdir(self.savepath):
            raise CommandError("--savepath option must specify a directory.")

        film_urls = []
        with io.StringIO() as fp:
            management.call_command("scrapefilmlist", verbosity=0, stdout=fp,
                                    url=self.url,
                                    page_size=self.page_size,
                                    start_page=self.start_page,
                                    max_pages=self.max_pages,
                                    )
            film_urls = fp.getvalue().splitlines()
        for url in film_urls:
            management.call_command("scrapefilm", url, verbosity=1, savepath=self.savepath)
