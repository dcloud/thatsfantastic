from django.conf.urls import url
from django.conf import settings
from cinema.views import (FilmDetail, FilmSearch, FilmList,
                          CountryFilmList, CountryList,
                          EventDetail, EventCountryFilmList)

CINEMA_DEFAULT_EVENT = getattr(settings, 'CINEMA_DEFAULT_EVENT', None)

app_name = 'cinema'
urlpatterns = [
    url(r'^events/(?P<slug>[\w\-]+)/$', EventDetail.as_view(), name='film-event-detail'),
    url(r'^events/(?P<event_slug>[\w\-]+)/country/(?P<country_slug>[\w\-\.]+)/$',
        EventCountryFilmList.as_view(), name='films-event-country'),
    url(r'^search/films/$', FilmSearch.as_view(), name='films-search'),
    url(r'^films/$', FilmList.as_view(), name='all-films-list'),
    url(r'^films/(?P<slug>[\w\-\.]+)/$', FilmDetail.as_view(), name='film-detail'),
    url(r'^countries/(?P<slug>[\w\-\.]+)/$', CountryFilmList.as_view(), name='films-from-country'),
    url(r'^countries/$', CountryList.as_view(), name='countries-from-films'),
    url(r'^$', EventDetail.as_view(), {'slug': CINEMA_DEFAULT_EVENT}, name='films-list'),
]
