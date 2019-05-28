from django.urls import path, re_path
from django.conf import settings
from cinema.views import (
    FilmDetail,
    FilmSearch,
    FilmList,
    CountryFilmList,
    CountryList,
    EventDetail,
    EventCountryFilmList,
)

CINEMA_DEFAULT_EVENT = getattr(settings, "CINEMA_DEFAULT_EVENT", None)

app_name = "cinema"
urlpatterns = [
    path("events/<slug:slug>/", EventDetail.as_view(), name="film-event-detail"),
    path(
        "events/<slug:title>/country/<slug:country>/",
        EventCountryFilmList.as_view(),
        name="films-event-country",
    ),
    path("search/films/", FilmSearch.as_view(), name="films-search"),
    path("films/", FilmList.as_view(), name="all-films-list"),
    re_path(r"^films/(?P<slug>[\w\-\.]+)/$", FilmDetail.as_view(), name="film-detail"),
    re_path(
        r"^countries/(?P<slug>[\w\-\.]+)/$",
        CountryFilmList.as_view(),
        name="films-from-country",
    ),
    path("countries/", CountryList.as_view(), name="countries-from-films"),
    path("", EventDetail.as_view(), {"slug": CINEMA_DEFAULT_EVENT}, name="films-list"),
]
