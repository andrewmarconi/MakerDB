"""
ASGI config for makerdb project.
It exposes the ASGI callable as a module-level variable named ``application``.
"""

import os
from django.core.asgi import get_asgi_application
from fastapi.staticfiles import StaticFiles

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "makerdb.settings")

# Initialize Django ASGI application early to ensure the AppRegistry is populated
# before importing code that may import models.
django_app = get_asgi_application()

from makerdb.api import app as fastapi_app

async def application(scope, receive, send):
    if scope["type"] == "http":
        # Mount FastAPI at /api
        if scope["path"].startswith("/api"):
            await fastapi_app(scope, receive, send)
            return

    # Fallback to Django
    await django_app(scope, receive, send)
