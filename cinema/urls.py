from django.conf.urls import patterns, url
from cinema.views import (FilmDetail, FilmSearch, FilmList, EventDetail)
from django.conf import settings

CINEMA_DEFAULT_EVENT = getattr(settings, 'CINEMA_DEFAULT_EVENT', None)


cinema_urlpatterns = patterns(
    'cinema',
    url(r'^events/(?P<slug>[\w\-]+)/$', EventDetail.as_view(), name='film-event-detail'),
    url(r'^search/films/$', FilmSearch.as_view(), name='films-search'),
    url(r'^films/$', FilmList.as_view(), name='all-films-list'),
    url(r'^films/(?P<slug>[\w\-\.]+)/$', FilmDetail.as_view(), name='film-detail'),
    url(r'^$', EventDetail.as_view(), {'slug': CINEMA_DEFAULT_EVENT}, name='films-list'),
)
