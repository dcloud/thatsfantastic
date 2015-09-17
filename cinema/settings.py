from django.conf import settings

CINEMA_DEFAULT_EVENT = getattr(settings, 'CINEMA_DEFAULT_EVENT', None)
