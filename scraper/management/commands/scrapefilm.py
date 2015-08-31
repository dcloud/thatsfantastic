from django.core.management.base import BaseCommand, CommandError
from django.core.management.color import no_style
from django.utils.termcolors import make_style
import argparse
from urllib.parse import urlparse
import os
import requests
import json
from scraper.scrape import FantasticMovieScraper


class Command(BaseCommand):
    """scrape a Fantatsic Fest film from a url"""

    def __init__(self, stdout=None, stderr=None, no_color=False):
        super(Command, self).__init__(stdout=stdout, stderr=stderr, no_color=no_color)
        self.info_style = make_style(fg='yellow') if self.stdout.isatty() else lambda x: x
        self.json_style = make_style(fg='blue') if self.stdout.isatty() else lambda x: x

    def _stdout_info(self, string):
        self.stdout.write(self.info_style(string))

    def _stdout_json(self, string):
        self.stdout.write(self.json_style(string))

    def add_arguments(self, parser):
        parser.add_argument('url', help='A URL to a Fantastic Fest movie detail page')
        parser.add_argument('--timeout', nargs='?', type=float, default=3.0,
                            help='Number of seconds to wait for a request to complete before giving up')
        parser.add_argument('-o', '--outfile', nargs='?', type=argparse.FileType('w'),
                            help='Write the output to a named file rather than stdout')
        parser.add_argument('--savepath', nargs='?',
                            help='Provide a path to a directory to save the file to. Exclusive from -o/--outfile.')

    def handle(self, *args, **options):
        self.verbosity = options['verbosity']
        self.url = options.get('url', None)
        self._stdout_info("Fetching {}".format(self.url))
        self.outfile = options.get('outfile', None)
        self.savepath = options.get('savepath', None)
        if self.savepath and not os.path.isdir(self.savepath):
            raise CommandError("--savepath option must specify a directory.")
        if self.outfile and self.savepath:
            raise CommandError('You may provide only an -o/--outfile or a --savepath, not both.')
        response = requests.request('GET', self.url, timeout=options['timeout'])
        if response.ok:
            if self.verbosity > 1:
                self.stdout.write("Fetched {}".format(self.url))
            movie_scraper = FantasticMovieScraper(response.content)
            obj = movie_scraper.scrape()
            url_slug = urlparse(response.url).path.split('/')[-1]
            if self.outfile:
                self._save_json(self.outfile, obj)
            elif self.savepath:
                filename = "{}.json".format(url_slug)
                fpath = os.path.join(os.path.abspath(self.savepath), filename)
                with open(fpath, 'w') as fp:
                    self._save_json(fp, obj)
            else:
                self._stdout_json(self._film_to_json_string(obj))

        else:
            self.stderr.write("Unable to GET {} [{}]'".format(self.url, response.status_code))

    def _save_json(self, fp, obj):
        json.dump(obj.data, fp, ensure_ascii=False)

    def _film_to_json_string(self, obj, indent=4):
        return json.dumps(obj.data, ensure_ascii=False, indent=indent)
