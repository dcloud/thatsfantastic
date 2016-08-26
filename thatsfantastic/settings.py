"""
Django settings for thatsfantastic project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

from django.conf.global_settings import \
            TEMPLATE_CONTEXT_PROCESSORS as DEFAULT_CONTEXT_PROCESSORS,\
            STATICFILES_FINDERS as DEFAULT_STATICFILES_FINDERS
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
DEBUG = True if os.getenv('DEBUG', 'False') == 'True' else False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'scraper',
    'cinema',
    'fantasticfest',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

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
            'context_processors': DEFAULT_CONTEXT_PROCESSORS,
            'debug': True if os.getenv('TEMPLATE_DEBUG', 'True') == 'True' else DEBUG
        }
    },
]

try:
    import debug_toolbar  # noqa F401
    if TEMPLATES[0]['OPTIONS']['debug'] is True:
        INSTALLED_APPS += ('debug_toolbar',)
except ImportError:
    pass

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

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'


SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
ALLOWED_HOSTS = ['*']

# Cinema settings
CINEMA_DEFAULT_EVENT = 'fantastic-fest-2015'
