from .base import *

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env("db_name"),
        "USER": env("db_user"),
        "PASSWORD": env("db_password"),
        "HOST": env("db_host"),
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES';",
        },
    }
}

SESSION_COOKIE_DOMAIN = "notifieee.ieeevit.org"

SESSION_COOKIE_SECURE = True
CRSF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

SECURE_HSTS_SECONDS = 31536000  # one Y
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
