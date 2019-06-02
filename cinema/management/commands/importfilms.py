from django.core.management.base import BaseCommand, CommandError
import os.path
from os import listdir
import json
from nameparser import HumanName
from cinema.models import Film, Person, Event, Country
from cinema.utils import titlecase


class Command(BaseCommand):
    """Load film data from a directory path or file."""

    def add_arguments(self, parser):
        parser.add_argument(
            "path",
            help="A path to a directory of JSON files or \
                                  single file with film data.",
        )
        parser.add_argument(
            "--event", nargs="?", help="Slug for an event to associate this film with."
        )
        parser.add_argument("-n", "--dry-run", action="store_true", dest="dryrun")

    def handle(self, *args, **options):
        self.verbosity = options["verbosity"]
        self.dryrun = options["dryrun"]
        self.event = options.get("event", None)
        if self.dryrun:
            self.stdout.write("Dry run. Nothing will be created in the database.")
        if os.path.exists(options["path"]):
            path = os.path.abspath(options["path"])
            json_files = []
            if os.path.isdir(path):
                if self.verbosity > 0:
                    self.stdout.write("Examining JSON files at {}".format(path))
                json_files = [
                    os.path.join(path, f) for f in listdir(path) if f.endswith(".json")
                ]
            elif os.path.isfile(path):
                json_files = [path]
            for fpath in json_files:
                data = self._load_json(fpath)
                if not self.dryrun:
                    self._create_film_entry(data, fpath)
                if self.verbosity > 2:
                    self.stdout.write(json.dumps(data))
        else:
            raise CommandError("Path is not a valid path")

    def _create_film_entry(self, data, path):
        if isinstance(data, dict):
            (head, tail) = os.path.split(path)
            (name, ext) = os.path.splitext(tail)
            title = data.get("title", None)
            directors = self._process_directors(data.get("directors", []))
            if not title:
                raise CommandError("Film data has no title!")
            (instance, created) = Film.objects.get_or_create(
                slug=name, year=data.get("year", None)
            )
            instance.title = titlecase(title)
            instance.synopsis = data.get("synopsis", instance.synopsis)
            instance.description = data.get("description", instance.description)
            instance.runtime = data.get("runtime", instance.runtime)
            for country_name in set(data.get("countries", [])):
                (country, _) = Country.objects.get_or_create(name=country_name)
                instance.countries.add(country)

            instance.directors.set(directors)
            has_source_url = "meta" in data and "source_url" in data["meta"]
            if has_source_url:
                source_url = data["meta"]["source_url"]
                url_set = set(instance.related_urls)
                url_set.add(source_url)
                instance.related_urls = list(url_set)
            instance.save()
            if self.event:
                try:
                    event = Event.objects.get(slug=self.event)
                    event.films.add(instance)
                    if self.verbosity > 2:
                        self.stdout.write(
                            "Associated '{}' with '{}'".format(
                                instance.title, event.title
                            )
                        )
                except Event.DoesNotExist:
                    self.stderr.write(
                        "Record does not exist for slug '{}'".format(self.event)
                    )
            self.stdout.write(
                "{} film '{}'".format(
                    "Created" if created else "Updated", str(instance)
                )
            )
        else:
            self.stderr.write("Error reading film data from a non-dictionary instance")

    def _load_json(self, fpath):
        data = None
        if self.verbosity > 1:
            self.stdout.write("Loading '{}'".format(fpath))
        with open(fpath, "r") as fp:
            try:
                data = json.load(fp)
            except ValueError:
                self.stderr.write("'' appears to be invalid JSON. Skipping.")
        return data

    def _process_directors(self, directors_list):
        people = []
        for name_str in directors_list:
            name = HumanName(name_str)
            (instance, created) = Person.objects.get_or_create(
                first_name=name.first, middle_name=name.middle, last_name=name.last
            )
            if self.verbosity > 1:
                self.stdout.write(
                    "{} person '{}'".format(
                        "Created" if created else "Updated", str(instance)
                    )
                )
            people.append(instance)
        return people
