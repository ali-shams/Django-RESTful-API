import os

import moneyed
from django.utils.translation import gettext_lazy as _
from django.contrib.messages import constants as messages
from decouple import config

from .base import (
    BASE_DIR,
    DEFAULT_APPS,
    MIDDLEWARE,
)

# ############################### #
#         CUSTOM PROJECT          #
# ############################### #
LOCAL_APPS = [
    'warehouse',
    'painless',
    'account',
    'basket',
    'pages',
    'voucher',
    'logistic',
    'feedback',
]

THIRD_PARTY_PACKAGES = [
    # ############################### #
    #        DJANGO EXTENSIONS        #
    # ############################### #
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django.contrib.admindocs',
    'django.contrib.humanize',
    'django.contrib.postgres',

    # ############################### #
    #           EXTENSIONS            #
    # ############################### #
    # Model Packages
    'mptt',
    'django_countries',
    'django_mptt_admin',
    'djmoney',
    # Image Package
    'django_cleanup',
    'sorl.thumbnail',
    # Admin Packages
    'jalali_date',
    'import_export',
    'colorfield',
    'modeltranslation',
    # Text Editor
    'ckeditor',
    'ckeditor_uploader',
    # Template Pacckages
    'compressor',
    'django_better_admin_arrayfield',
    # Monitoring Packages
    # 'silk',

    # RESTful Packages
    'rest_framework',
    'django_filters',
    "drf_standardized_errors",
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'drf_yasg',
    'azbankgateways',
    # admin
    'django_admin_listfilter_dropdown',
]

DEFAULT_APPS.insert(0, 'dal')
DEFAULT_APPS.insert(1, 'dal_select2')
DEFAULT_APPS.insert(2, 'dal_admin_filters')
INSTALLED_APPS = DEFAULT_APPS + LOCAL_APPS + THIRD_PARTY_PACKAGES

# ############################### #
#           MIDDLEWARE            #
# ############################### #
# To add documentation support in Django admin
MIDDLEWARE.append('django.contrib.admindocs.middleware.XViewMiddleware')
MIDDLEWARE.insert(3, 'django.middleware.locale.LocaleMiddleware')
MIDDLEWARE.append('htmlmin.middleware.HtmlMinifyMiddleware')
MIDDLEWARE.append('htmlmin.middleware.MarkRequestMiddleware')
# MIDDLEWARE.append('silk.middleware.SilkyMiddleware')

# ############################### #
#             MESSAGE             #
# ############################### #
MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

# ############################### #
#         DEBUG CONFIG            #
# ############################### #
if config('DEBUG', default=False, cast=bool):
    INSTALLED_APPS.append('django_extensions')

# ############################### #
#             LOCALE              #
# ############################### #
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)
MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'
MODELTRANSLATION_LANGUAGES = (
    'en',
    'fa'
)
LANGUAGE_CODE = 'en'  # default language
LANGUAGES = (
    ('en', 'en-US'),
    ('fa', 'fa-IR'),
)

# ############################### #
#          MPTT PACKAGE           #
# ############################### #
MPTT_ADMIN_LEVEL_INDENT = 20

# ############################### #
#            MINIFERS             #
# ############################### #
COMPRESS_ENABLED = config('COMPRESS_ENABLED', cast=bool)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)
HTML_MINIFY = config('HTML_MINIFIER', cast=bool)
KEEP_COMMENTS_ON_MINIFYING = False

# ######################## #
#           SILK           #
# ######################## #
# SILKY_ANALYZE_QUERIES = True
# SILKY_META = True
# SILKY_PYTHON_PROFILER = True
# SILKY_PYTHON_PROFILER_BINARY = True


# ######################## #
#           MPTT           #
# ######################## #
MPTT_ADMIN_LEVEL_INDENT = 20
# ############################### #
#           THUMBNAIL             #
# ############################### #
if config('DEBUG', default=False, cast=bool):
    THUMBNAIL_DEBUG = True
else:
    THUMBNAIL_DEBUG = False

THUMBNAIL_KEY_PREFIX = config('THUMBNAIL_KEY_PREFIX')
THUMBNAIL_PREFIX = config('THUMBNAIL_PREFIX')
THUMBNAIL_FORMAT = config('THUMBNAIL_FORMAT')
THUMBNAIL_PRESERVE_FORMAT = config('THUMBNAIL_PRESERVE_FORMAT', cast=bool)

# ############################### #
#         Django MONEY            #
# ############################### #
RIAL = moneyed.add_currency(
    code='R',
    numeric='095',
    name=_('Iranian Rial'),
    countries=('Iran',)
)
TOMAN = moneyed.add_currency(
    code='T',
    numeric='095',
    name=_('Iranian Toman'),
    countries=('Iran',)
)
CURRENCIES = (
    'R',
    'T',
    'USD'
)
DEFAULT_CURRENCY_SHOW_ON_SITE = 'T'
USE_THOUSAND_SEPARATOR = True
# ############################### #
#         AUTHENTICATION          #
# ############################### #
AUTH_USER_MODEL = 'account.User'
LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# ############################### #
#               DRF               #
# ############################### #

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '1000/day',
        'user': '10000/day'
    },
    # other settings
    "EXCEPTION_HANDLER": "drf_standardized_errors.handler.exception_handler"
}

if not config('DEBUG', default=False, cast=bool):
    REST_FRAMEWORK.update({
            'DEFAULT_RENDERER_CLASSES': (
                'rest_framework.renderers.JSONRenderer',
            ),
        }
    )
    # allow you to get more information out of the traceback on DEBUG=True
    DRF_STANDARDIZED_ERRORS = {"ENABLE_IN_DEBUG_FOR_UNHANDLED_EXCEPTIONS": True}


# ############################### #
#            CK Editor            #
# ############################### #
CKEDITOR_UPLOAD_PATH = 'uploads/ckeditor/'
CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        # 'skin': 'office2013',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            {'name': 'forms',
             'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                       'HiddenField']},
            '/',
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                       'Language']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert',
             'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
            {'name': 'about', 'items': ['About']},
            '/',  # put this to force next toolbar on new line
            {'name': 'yourcustomtools', 'items': [
                # put the name of your editor.ui.addButton here
                'Preview',
                'Maximize',

            ]},
        ],
        'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
        # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
        # 'height': 291,
        # 'width': '100%',
        # 'filebrowserWindowHeight': 725,
        # 'filebrowserWindowWidth': 940,
        # 'toolbarCanCollapse': True,
        # 'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage',  # the upload image feature
            # your extra plugins here
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            # 'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
    }
}

# ############################### #
#            SITE MAP             #
# ############################### #
SITE_ID = 1


AZ_IRANIAN_BANK_GATEWAYS = {
   'GATEWAYS': {
       'IDPAY': {
           'MERCHANT_CODE': config('ID_PAY_MERCHANT_CODE', cast=str),
           'METHOD': 'POST',  # GET or POST
           'X_SANDBOX': 1,  # 0 disable, 1 active
       },
   },
   'IS_SAMPLE_FORM_ENABLE': True,  # optional
   'DEFAULT': 'IDPAY',
   'CURRENCY': 'IRR',  # optional
   'TRACKING_CODE_QUERY_PARAM': 'tn',  # optional
   'TRACKING_CODE_LENGTH': 16,  # optional
   'SETTING_VALUE_READER_CLASS': 'azbankgateways.readers.DefaultReader',  # optional
   'BANK_PRIORITIES': [],
}

# ######################## #
#   DJANGO DEBUG TOOLBAR   #
# ######################## #
if config("DEBUG_TOOLBAR", default=False, cast=bool):
    import mimetypes
    mimetypes.add_type("application/javascript", ".js", True)

    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
    # INTERNAL_IPS = config('CORS_ALLOWED_ORIGINS', cast=lambda v: [s.strip() for s in v.split(',')])

    def show_toolbar(request):
        return True

    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": show_toolbar,
    }