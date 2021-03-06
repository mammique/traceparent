# -*- coding: utf-8 -*-
# Django settings for traceparent project.
import os, commands

PROJECT_FSPATH           = os.path.dirname(os.path.abspath(__file__))
PROJECT_NAME             = 'Traceparent'
PROJECT_URL              = 'http://traceparent.com/'
PROJECT_VERSION          = '0.1-beta'
PROJECT_VERSION_REVISION = '???'

try: PROJECT_VERSION_REVISION = commands.getstatusoutput('git reflog')[1].split(' ')[0]
except: pass

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
#        'STORAGE_ENGINE': 'MyISAM', # For MySQL.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = False

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = 'static/' # os.path.join(os.path.dirname(PROJECT_FSPATH), 'static'),

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_FSPATH, 'static'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
)

ROOT_URLCONF = 'traceparent.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'traceparent.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_FSPATH, 'templates'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# https://github.com/django/django/blob/384c180e414a982a6cc5ccabc675bcfb4fd80988/django/conf/global_settings.py#L204
TEMPLATE_CONTEXT_PROCESSORS = (
    'traceparent.contexts.settings',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
#    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)

AUTH_USER_MODEL = 'tp_auth.User'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
#    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',

    # Traceparent deps:
    'rest_framework',
    'rest_framework.authtoken',
    'django_extensions',
    'south',
    'corsheaders',

    # Traceparent apps:
    'tp_auth',
    'tp_value',
    'tp_metadata',
    'tp_monitor',

    # Extra apps:
    'extra_serve',
    'extra_misc',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

REST_FRAMEWORK = {
    'FILTER_BACKEND': 'rest_framework.filters.DjangoFilterBackend',
    #'FILTER_BACKEND': 'traceparent.filters.NoneDjangoFilterBackend',
    'PAGINATE_BY': 20,
    'PAGINATE_BY_PARAM': 'page_size',
    'DEFAULT_AUTHENTICATION_CLASSES': (
#        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'traceparent.renderers.BrowsableAPIRenderer',
        'traceparent.renderers.FormRenderer',
    ),
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = (
    'GET',
#    'POST',
#    'PUT',
#    'PATCH',
#    'DELETE',
    'OPTIONS'
)

TP_EXTERNAL_UI_URI = ''

TP_VALUE_QUANTITY_MAX_DIGITS              = 64 # 128
TP_VALUE_QUANTITY_DECIMAL_PLACES          = 30 # 64
#TP_VALUE_QUANTITY_DECIMAL_PLACES_QUANTIZE = Decimal(10) ** -VALUE_QUANTITY_DECIMAL_PLACES
TP_VALUE_QUANTITY_DECIMAL_MODEL_ATTRS     = {
    'max_digits': TP_VALUE_QUANTITY_MAX_DIGITS,
    'decimal_places': TP_VALUE_QUANTITY_DECIMAL_PLACES
}

EXTRA_SERVE_NGINX_INTERNAL_URL = '/internal/extra/serve'
EXTRA_SERVE_NGINX_ROOT         = os.path.abspath(os.path.join(PROJECT_FSPATH, '../../../var/extra/serve'))

try:
    from settings_local import *
except ImportError:
    pass
