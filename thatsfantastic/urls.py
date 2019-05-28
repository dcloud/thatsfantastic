from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.contrib import admin

urlpatterns = [path("", include("cinema.urls")), path("admin/", admin.site.urls)]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
