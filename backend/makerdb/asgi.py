"""
ASGI config for makerdb project.
"""

import os
from django.core.asgi import get_asgi_application
from fastapi import FastAPI

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "makerdb.settings")

django_app = get_asgi_application()

from makerdb.api import app as fastapi_app

application = FastAPI(openapi_url=None, docs_url=None, redoc_url=None)

admin_asgi = get_asgi_application()
application.mount("/", admin_asgi)

application.mount("/api", fastapi_app)
