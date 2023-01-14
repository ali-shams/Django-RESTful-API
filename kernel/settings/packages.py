import os

from django.contrib.messages import constants as messages
from decouple import config

from .base import (
    BASE_DIR,
    DEFAULT_APPS,
    MIDDLEWARE,
)

# ############################### #
#           CUSTOM APPS           #
# ############################### #
LOCAL_APPS = [
    "painless",
    "apps.account"
]

THIRD_PARTY_PACKAGES = [
    # ############################### #
    #        DJANGO EXTENSIONS        #
    # ############################### #
    "django.contrib.sitemaps",
    "django.contrib.sites",
    "django.contrib.admindocs",
    "django.contrib.humanize",
    "django.contrib.postgres",

    # ############################### #
    #           EXTENSIONS            #
    # ############################### #
    # RESTful API Packages
    'rest_framework',
    'knox',
]

INSTALLED_APPS = DEFAULT_APPS + LOCAL_APPS + THIRD_PARTY_PACKAGES

# ############################### #
#           MIDDLEWARE            #
# ############################### #
# To add documentation support in Django admin
MIDDLEWARE.append("django.contrib.admindocs.middleware.XViewMiddleware")

# ############################### #
#             MESSAGE             #
# ############################### #
MESSAGE_TAGS = {
    messages.DEBUG: "debug",
    messages.INFO: "info",
    messages.SUCCESS: "success",
    messages.WARNING: "warning",
    messages.ERROR: "danger",
}

# ############################### #
#             LOCALE              #
# ############################### #
LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale"),
)

LANGUAGE_CODE = config("LANGUAGE_CODE")
LANGUAGES = eval(config("LANGUAGES"))

# ############################### #
#            SITE MAP             #
# ############################### #
SITE_ID = 1

# ############################### #
#         AUTHENTICATION          #
# ############################### #
AUTH_USER_MODEL = "account.User"

# ############################### #
#               DRF               #
# ############################### #
REST_FRAMEWORK = {
    # 'EXCEPTION_HANDLER': 'painless.api.exceptions.custom_exception_handler',
    'DEFAULT_AUTHENTICATION_CLASSES': ('knox.auth.TokenAuthentication',),
}

# ############################### #
#         REDIS CONFIGS           #
# ############################### #
REDIS_HOST = config('REDIS_HOST')
REDIS_PORT = config('REDIS_PORT')
REDIS_DB = config('REDIS_DB')
CACHE_TTL = 10 * 60  # seconds

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
