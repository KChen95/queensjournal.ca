import os
from settings import *
# JOURNAL DEPLOYMENT SETTINGS
# These are for reference/or in case the server ever blows up.
# You'll need to put this on the server and rename it to settings_local.py and fill in the Database section, which is left blank for security reasons.

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

MEDIA_URL = '/media/' # TODO change on prod

STATIC_URL = '/static/' # TODO change on prod

SECRET_KEY = 'jqb%^1wtw4#g2ug8w^shcm=&o)$^dx7$os3cnbexpy@607vuwu'

HAYSTACK_XAPIAN_PATH = os.path.join(PROJECT_ROOT, 'xapian/')

# Twitter Authentication info for posting new stories to Twitter
# Visit dev.twitter.com for more info.

TWITTER_CONSUMER_KEY = 'PjgX8fatfPZpni8LfDsw'
TWITTER_CONSUMER_SECRET ='I7ApkCNAAZXzeUw2KdDLbjj33a2kKL7Vj5n2smGq1l4'
TWITTER_ACCESS_TOKEN_KEY ='16619266-pqQxfmoRhVJ0DdTmQGe21F3YuWXaE1cjtc521rj04'
TWITTER_ACCESS_TOKEN_SECRET ='c0i5AX2cGtbvpeJv96FH6viQ9hEBo6COqIk3kFXNM'

TWITTER_DEV = False

# MEMCACHED Config
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 60,
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}

EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = 'server@queensjournal.ca'
SERVER_EMAIL = 'server@queensjournal.ca'

SHORT_BASE_URL = "http://qjrnl.net/"
SHORTEN_FULL_BASE_URL = "http://queensjournal.ca/"
