"""
ASGI config for makerdb project.
"""

import os
from django.core.asgi import get_asgi_application
from fastapi import FastAPI

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "makerdb.settings")

# 1. Initialize Django ASGI application
# This must happen before importing any models or the FastAPI app if it uses models
django_app = get_asgi_application()

# 2. Import the FastAPI app
from makerdb.api import app as fastapi_app

# 3. Create the top-level ASGI application
# OpenAPI is disabled here as it's handled by the sub-app
application = FastAPI(openapi_url=None, docs_url=None, redoc_url=None)

# 4. Mount FastAPI at /api
# Starlette/FastAPI's mount handles path stripping and root_path automatically.
# Request to /api/parts -> handled by fastapi_app as /parts
application.mount("/api", fastapi_app)

# 5. Mount Django at the root as a fallback
application.mount("/", django_app)
