from decouple import config

from .base import *
from .secure import *
from .packages import *

DEBUG = True
ALLOWED_HOSTS = config("ALLOWED_HOSTS",
                       cast=lambda v: [s.strip() for s in v.split(",")])
