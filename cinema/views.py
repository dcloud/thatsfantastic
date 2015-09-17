from django.views.generic import (ListView, DetailView)
from django.views.generic.detail import SingleObjectMixin
from django.db.models import Q

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
        title_q = Q(title__icontains=self.query)
        description_q = Q(description__icontains=self.query)
        year = self.request.GET.get("year", None)
        qs = self.model.objects.filter(title_q | description_q)
        if year:
            try:
                year_val = int(year)
                qs = qs.filter(year=year_val)
            except ValueError:
                pass
        return qs

    def get_context_data(self, **kwargs):
        context = super(FilmSearch, self).get_context_data(**kwargs)
        context['q'] = self.query
        return context


class CountryFilmList(FilmList):
    """Filter Films by a country name slug"""

    def get_queryset(self):
        country_slug = self.kwargs.get('slug')
        self.name_approx = country_slug.replace('-', ' ').title()
        return Film.objects.filter(countries__contains=[self.name_approx]).order_by('shown_at')

    def get_context_data(self, **kwargs):
        context = super(CountryFilmList, self).get_context_data(**kwargs)
        context['country'] = self.name_approx
        return context


class CountryList(ListView):
    """List of countries with associated films"""
    model = Country


class EventDetail(SingleObjectMixin, FilmList):
    model = Event

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Event.objects.all())
        return super(EventDetail, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EventDetail, self).get_context_data(**kwargs)
        context['event'] = self.object
        return context

    def get_queryset(self):
        return self.object.films.all()
