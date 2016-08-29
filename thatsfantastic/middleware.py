from django.utils.deprecation import MiddlewareMixin
from debug_toolbar.middleware import DebugToolbarMiddleware


# FIXME: A temporary fix for DebugToolbarMiddleware. Look for a 1.5.x release 
# https://github.com/jazzband/django-debug-toolbar/issues/853
class CompatitibleWith110DebugMiddleware(MiddlewareMixin, DebugToolbarMiddleware):
    pass
