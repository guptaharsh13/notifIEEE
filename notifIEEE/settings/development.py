from .base import *

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", env("NGROK_URL")]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "notifIEEEdb",
        "USER": "root",
        "PASSWORD": env("db_password_development"),
        "HOST": "localhost",
        "PORT": 3306,
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES';",
        },
    }
}
