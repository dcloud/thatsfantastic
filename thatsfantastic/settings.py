"""
Django settings for thatsfantastic project.
"""

from datetime import date
import dj_database_url
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
PROJ_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(PROJ_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', None)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'
DEBUG_TOOLBAR = os.getenv('DEBUG_TOOLBAR', 'False') == 'True'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django.contrib.postgres',

    'scraper',
    'cinema',
    'fantasticfest',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG and DEBUG_TOOLBAR:
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.append('thatsfantastic.middleware.CompatitibleWith110DebugMiddleware')  # FIXME: Need 1.5.x release of debug-toolbar

ROOT_URLCONF = 'thatsfantastic.urls'

WSGI_APPLICATION = 'thatsfantastic.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config()
}

# Templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [os.path.join(PROJ_DIR, 'templates')],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'cinema.context_processors.cinema',
            ],
            'debug': os.getenv('TEMPLATE_DEBUG', 'False') == 'True'
        }
    },
]

# DEBUG TOOLBAR
DEBUG_TOOLBAR_PATCH_SETTINGS = False
INTERNAL_IPS = [
    '127.0.0.1',
    '::1',
]
# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = False

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = (
    os.path.join(PROJ_DIR, 'static'),
)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
ALLOWED_HOSTS = ['*']


def calculate_event_slug(name):
    now = date.today()
    year = now.year if now.month > 7 else now.year - 1
    name_parts = name.lower().split() + [str(year)]
    return '-'.join(name_parts)

# Cinema settings

CINEMA_DEFAULT_EVENT = os.getenv('CINEMA_DEFAULT_EVENT', calculate_event_slug('Fantastic Fest'))
