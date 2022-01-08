from django.core.wsgi import get_wsgi_application
import os
import environ
from pathlib import Path

path = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(env_file=os.path.join(path, ".env"))


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", f'notifieee.settings.{env("django_env")}'
)

application = get_wsgi_application()
