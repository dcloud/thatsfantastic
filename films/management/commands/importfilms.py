from django.core.management.base import BaseCommand, CommandError
from films.models import Film, Person
import os.path
from os import listdir
import json
from nameparser import HumanName
from django_countries import countries


class Command(BaseCommand):
    """Load film data from a directory path or file."""

    def add_arguments(self, parser):
        parser.add_argument('path',
                            help='A path to a directory of JSON files or \
                                  single file with film data.')
        parser.add_argument('-n', '--dry-run', action='store_true', dest='dryrun')

    def handle(self, *args, **options):
        self.verbosity = options['verbosity']
        self.dryrun = options['dryrun']
        if self.dryrun:
            self.stdout.write("Dry run. Nothing will be created in the database.")
        if os.path.exists(options['path']):
            path = os.path.abspath(options['path'])
            json_files = []
            if os.path.isdir(path):
                json_files = [os.path.join(path, f) for f in listdir(path) if f.endswith('.json')]
            elif os.path.isfile(path):
                json_files = [path]
            for fpath in json_files:
                data = self._load_json(fpath)
                if not self.dryrun:
                    self._create_film_entry(data, fpath)
                if self.verbosity > 2:
                    self.stdout.write(json.dumps(data))
        else:
            raise CommandError('Path is not a valid path')

    def _create_film_entry(self, data, path):
        if isinstance(data, dict):
            (head, tail) = os.path.split(path)
            (name, ext) = os.path.splitext(tail)
            countries_abbrs = (self._lookup_country(c) for c in data.get('countries', []))
            directors = self._process_directors(data.get('directors', []))
            (object, created) = Film.objects\
                .get_or_create(title=data.get('title', None),
                               slug=name,
                               synopsis=data.get('synopsis', ''),
                               description=data.get('description', ''),
                               runtime=data.get('runtime', None),
                               year=data.get('year', None),
                               )
            object.countries = [c for c in countries_abbrs if c]
            object.directors = directors
            object.save()
            self.stdout.write("{} film '{}'".format('Created' if created else 'Updated', str(object)))
        else:
            self.stderr.write("Error reading film data from a non-dictionary object")

    def _load_json(self, fpath):
        data = None
        if self.verbosity > 1:
            self.stdout.write("Loading '{}'".format(fpath))
        with open(fpath, 'r') as fp:
            try:
                data = json.load(fp)
            except ValueError:
                self.stderr.write("'' appears to be invalid JSON. Skipping.")
        return data

    def _lookup_country(self, name):
        if name == 'United States':
            return 'US'
        return countries.by_name(name)

    def _process_directors(self, directors_list):
        people = []
        for name_str in directors_list:
            name = HumanName(name_str)
            (object, created) = Person.objects.get_or_create(first_name=name.first,
                                                             middle_name=name.middle,
                                                             last_name=name.last)
            if self.verbosity > 1:
                self.stdout.write("{} person '{}'".format('Created' if created else 'Updated', str(object)))
            people.append(object)
        return people
