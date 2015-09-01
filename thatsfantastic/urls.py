from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from cinema.urls import cinema_urlpatterns

DEBUG = getattr(settings, 'DEBUG', False)

urlpatterns = patterns(
    '',
    url(r'^', include(cinema_urlpatterns)),
    url(r'^admin/', include(admin.site.urls)),
)


if DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
