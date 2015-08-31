from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from cinema.views import (FilmDetailView, FilmSearchView, FilmListView)

DEBUG = getattr(settings, 'DEBUG', False)

urlpatterns = patterns('',
    url(r'^search/films/$', FilmSearchView.as_view(), name='films-search'),
    url(r'^films/(?P<slug>[\w\-\.]+)/$', FilmDetailView.as_view(), name='film-detail'),
    url(r'^$', FilmListView.as_view(), name='films-list'),

    url(r'^admin/', include(admin.site.urls)),
)


if DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
