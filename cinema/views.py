from django.views.generic import ListView, DetailView
from django.contrib.postgres.search import (
    SearchQuery,
    SearchRank,
    SearchVector,
    TrigramSimilarity,
)
from django.conf import settings
from cinema.models import Film, Event, Country

CINEMA_DEFAULT_EVENT = getattr(settings, "CINEMA_DEFAULT_EVENT", None)

QUOTE_MARKS = ('"', "'")


class FilmDetail(DetailView):
    model = Film


class FilmList(ListView):
    model = Film

    def get_context_data(self, **kwargs):
        context = super(FilmList, self).get_context_data(**kwargs)
        context["default_event"] = CINEMA_DEFAULT_EVENT
        return context


class FilmSearch(FilmList):
    model = Film

    def get_queryset(self):
        self.query = self.request.GET.get("q")
        year = self.request.GET.get("year", None)
        query = None
        ordering = ("title", "id")
        distinct_on = ("title", "id")
        is_quoted = (self.query[0] in QUOTE_MARKS) and self.query[0] == self.query[-1]
        if is_quoted:
            query = SearchQuery(self.query)
        else:
            query_words = self.query.split()
            query = SearchQuery(query_words[0])
            for word in query_words[1:]:
                query.bitor(SearchQuery(word))
        vector = (
            SearchVector("title", weight="A")
            + SearchVector("description", weight="C")
            + SearchVector("directors__last_name", weight="B")
            + SearchVector("countries__name", weight="B")
        )
        qs = self.model.objects.annotate(rank=SearchRank(vector, query)).filter(
            rank__gte=0.12
        )
        if qs.count() != 0:
            ordering = ("-rank",) + ordering
            distinct_on = ("rank",) + distinct_on
        else:
            qs = Film.objects.annotate(
                similarity=TrigramSimilarity("title", self.query)
            ).filter(similarity__gt=0.25)
            ordering = ("-similarity",) + ordering
            distinct_on = ("similarity",) + distinct_on

        if year:
            try:
                year_val = int(year)
                qs = qs.filter(year=year_val)
            except ValueError:
                pass

        return qs.order_by(*ordering).distinct(*distinct_on)

    def get_context_data(self, **kwargs):
        context = super(FilmSearch, self).get_context_data(**kwargs)
        context["q"] = self.query
        return context


class CountryFilmList(FilmList):
    """Filter Films by a country name slug"""

    paginate_by = 20

    def get_queryset(self):
        country_slug = self.kwargs.get("slug")
        self.country = Country.objects.get(slug=country_slug)
        return self.country.film_set.all().order_by("-shown_at__start_day", "title")

    def get_context_data(self, **kwargs):
        context = super(CountryFilmList, self).get_context_data(**kwargs)
        context["country"] = self.country
        return context


class CountryList(ListView):
    """List of countries with associated films"""

    model = Country


class EventDetail(DetailView):
    model = Event


class EventCountryFilmList(CountryFilmList):
    def get_queryset(self):
        event_slug = self.kwargs.get("event_slug")
        country_slug = self.kwargs.get("country_slug")
        self.country = Country.objects.get(slug=country_slug)
        self.event = Event.objects.get(slug=event_slug)
        return self.country.film_set.filter(shown_at=self.event).order_by("shown_at")

    def get_context_data(self, **kwargs):
        context = super(CountryFilmList, self).get_context_data(**kwargs)
        context["country"] = self.country
        context["event"] = self.event
        return context
