from django.views.generic import (ListView, DetailView)
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from cinema.models import (Film, Event, Country)
from cinema.settings import CINEMA_DEFAULT_EVENT


class FilmDetail(DetailView):
    model = Film


class FilmList(ListView):
    model = Film

    def get_context_data(self, **kwargs):
        context = super(FilmList, self).get_context_data(**kwargs)
        context['default_event'] = CINEMA_DEFAULT_EVENT
        return context


class FilmSearch(FilmList):
    model = Film

    def get_queryset(self):
        self.query = self.request.GET.get("q")
        query = None
        if (self.query[0] == "'" or self.query[0] == '"') and self.query[0] == self.query[-1]:
            query = SearchQuery(self.query)
        else:
            query_words = self.query.split()
            query = SearchQuery(query_words[0])
            for word in query_words[1:]:
                query.bitor(SearchQuery(word))
        vector = (
            SearchVector('title', weight='A') +
            SearchVector('description', weight='C') +
            SearchVector('directors__last_name', weight='B') +
            SearchVector('countries__name', weight='B')
        )
        qs = self.model.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.12)

        year = self.request.GET.get("year", None)
        if year:
            try:
                year_val = int(year)
                qs = qs.filter(year=year_val)
            except ValueError:
                pass

        qs = qs.order_by('-rank', 'title', 'id').distinct('rank', 'title', 'id')
        return qs

    def get_context_data(self, **kwargs):
        context = super(FilmSearch, self).get_context_data(**kwargs)
        context['q'] = self.query
        return context


class CountryFilmList(FilmList):
    """Filter Films by a country name slug"""
    paginate_by = 20

    def get_queryset(self):
        country_slug = self.kwargs.get('slug')
        self.country = Country.objects.get(slug=country_slug)
        return self.country.film_set.all().order_by('shown_at')

    def get_context_data(self, **kwargs):
        context = super(CountryFilmList, self).get_context_data(**kwargs)
        context['country'] = self.country
        return context


class CountryList(ListView):
    """List of countries with associated films"""
    model = Country


class EventDetail(DetailView):
    model = Event


class EventCountryFilmList(CountryFilmList):

    def get_queryset(self):
        event_slug = self.kwargs.get('event_slug')
        country_slug = self.kwargs.get('country_slug')
        self.country = Country.objects.get(slug=country_slug)
        self.event = Event.objects.get(slug=event_slug)
        return self.country.film_set.filter(shown_at=self.event).order_by('shown_at')

    def get_context_data(self, **kwargs):
        context = super(CountryFilmList, self).get_context_data(**kwargs)
        context['country'] = self.country
        context['event'] = self.event
        return context
