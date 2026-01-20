# Development Workflow

## ASGI Application Architecture

The application uses a hybrid architecture defined in [backend/makerdb/asgi.py](../../../backend/makerdb/asgi.py):

```python
# Simplified view of asgi.py
django_app = get_asgi_application()
from makerdb.api import app as fastapi_app

application = FastAPI(openapi_url=None, docs_url=None, redoc_url=None)
application.mount("/api", fastapi_app)

admin_asgi = get_asgi_application()
application.mount("/cp", admin_asgi)
```

This means:
- **FastAPI** handles all `/api/*` routes
- **Django** handles `/cp/*` (admin panel)
- Both share the same process, database connection, and authentication

## FastAPI Router Registration

All routers are registered in [backend/makerdb/api.py](../../../backend/makerdb/api.py):

```python
from fastapi import FastAPI
from parts.router import router as parts_router
from inventory.router import router as inventory_router
# ... more imports

app = FastAPI(title="MakerDB API", version="0.1.0")

app.include_router(parts_router)
app.include_router(inventory_router)
# ... more routers
```

## Async Pattern with Django ORM

FastAPI endpoints are async, but Django ORM is synchronous. Use `sync_to_async` from `asgiref.sync`:

```python
from asgiref.sync import sync_to_async
from fastapi import APIRouter, HTTPException
from .models import Part

router = APIRouter(prefix="/parts", tags=["Parts"])

@router.get("/")
async def list_parts():
    parts = await sync_to_async(list)(Part.objects.all())
    return parts

@router.get("/{part_id}")
async def get_part(part_id: UUID):
    try:
        part = await sync_to_async(Part.objects.get)(id=part_id)
        return part
    except Part.DoesNotExist:
        raise HTTPException(status_code=404, detail="Part not found")
```

For complex operations, wrap in a function:

```python
@router.post("/")
async def create_part(data: PartCreate):
    @sync_to_async
    def _create():
        part = Part(**data.model_dump())
        part.save()
        return part

    return await _create()
```
