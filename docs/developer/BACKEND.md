# Backend Development Guide

This guide covers everything you need to know to develop and contribute to the MakerDB backend application.

## Table of Contents

- [Overview](#overview)
- [Technology Stack](#technology-stack)
- [Package Overview](#package-overview)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Data Models](#data-models)
- [API Development](#api-development)
- [Testing](#testing)
- [Database Management](#database-management)
- [Coding Conventions](#coding-conventions)
- [Common Tasks](#common-tasks)

## Overview

The MakerDB backend uses a hybrid architecture combining **Django 6.0.1** for ORM, admin, and migrations with **FastAPI** for high-performance REST API endpoints. Both frameworks run in a single ASGI process, sharing authentication and database access.

### Key Features
- Hybrid Django + FastAPI architecture
- Type-safe API with Pydantic validation
- Async-capable FastAPI endpoints
- Django admin panel with Jazzmin theme
- PostgreSQL 17 database
- Comprehensive test coverage with pytest

## Technology Stack

### Core Frameworks
- **Django 6.0.1** - ORM, migrations, admin panel, authentication
- **FastAPI** (`^0.128.0`) - Modern async web framework for APIs
- **Uvicorn** (`^0.40.0`) - ASGI server with auto-reload

### Database
- **PostgreSQL 17** - Primary database (via Docker Compose)
- **psycopg[binary]** (`^3.3.2`) - PostgreSQL adapter for Python

### Configuration & Utilities
- **django-environ** (`^0.12.0`) - Environment variable management
- **django-jazzmin** (`^3.0.1`) - Modern Django admin theme
- **python-multipart** (`^0.0.20`) - Multipart form data parsing
- **whitenoise** (`^6.8.0`) - Static file serving

### Development Tools
- **pytest** (`^9.0.2`) - Testing framework
- **pytest-django** (`^4.11.1`) - Django plugin for pytest
- **ruff** (`^0.14.13`) - Fast Python linter and formatter

### Package Manager
- **uv** - Modern, fast Python package manager (replaces pip/poetry/pipenv)

## Package Overview

### Django 6.0.1
Provides the foundation of the application:
- **ORM**: Object-relational mapping with support for complex queries
- **Migrations**: Schema versioning and management
- **Admin**: Auto-generated admin interface (enhanced with Jazzmin)
- **Authentication**: Built-in user authentication system
- **Middleware**: Request/response processing

**Documentation**: https://docs.djangoproject.com/

### FastAPI
High-performance async framework for building APIs:
- **Automatic OpenAPI/Swagger documentation**
- **Pydantic validation** - Type-safe request/response schemas
- **Async support** - Native async/await for I/O operations
- **Dependency injection** - Clean, testable code architecture
- **High performance** - Built on Starlette and Pydantic

**Documentation**: https://fastapi.tiangolo.com/

### Pydantic
Data validation using Python type annotations:
- Automatic request/response validation
- Clear error messages
- Editor support with autocomplete
- Serialization/deserialization

### pytest & pytest-django
Modern testing framework:
- Fixture-based test architecture
- Parallel test execution
- Database transaction handling
- Django-specific assertions and utilities

**Documentation**: https://docs.pytest.org/ & https://pytest-django.readthedocs.io/

### Ruff
Fast linter and formatter that replaces multiple tools:
- Linting (replaces flake8, pylint)
- Formatting (replaces black)
- Import sorting (replaces isort)
- ~10-100x faster than alternatives

**Documentation**: https://docs.astral.sh/ruff/

## Project Structure

```
backend/
├── makerdb/                 # Django project directory
│   ├── __init__.py
│   ├── settings.py         # Django settings (uses django-environ)
│   ├── urls.py             # Django URL configuration
│   ├── asgi.py            # ASGI application (mounts FastAPI + Django)
│   └── api.py             # FastAPI router registration
├── core/                   # Core models and utilities
│   ├── models.py          # TimeStampedModel, GlobalOpsBase, Company, Attachment
│   ├── router.py          # Core API endpoints
│   ├── schemas.py         # Pydantic schemas
│   ├── admin.py           # Django admin configuration
│   └── apps.py            # Django app configuration
├── parts/                  # Parts management
│   ├── models.py          # Part, Designator models
│   ├── router.py          # Parts CRUD endpoints
│   ├── schemas.py         # Pydantic schemas
│   └── admin.py           # Admin configuration
├── inventory/              # Inventory and storage
│   ├── models.py          # Storage, Lot, Stock models
│   ├── router.py          # Inventory endpoints
│   ├── schemas.py         # Pydantic schemas
│   └── admin.py
├── projects/               # Projects and BOMs
│   ├── models.py          # Project, BOMItem models
│   ├── router.py          # Project endpoints
│   ├── schemas.py
│   └── admin.py
├── procurement/            # Procurement management
│   ├── models.py          # Order, Offer models
│   ├── router.py          # Procurement endpoints
│   ├── schemas.py
│   └── admin.py
├── tests/                  # Test directory
│   ├── conftest.py        # Pytest configuration and fixtures
│   ├── test_models.py     # Model tests
│   ├── test_api.py        # API endpoint tests
│   └── ...
└── manage.py               # Django management script
```

### Django App Pattern

Each Django app follows a consistent structure:

1. **models.py** - Django ORM models
2. **schemas.py** - Pydantic schemas for API validation
3. **router.py** - FastAPI router with CRUD endpoints
4. **admin.py** - Django admin configuration
5. **apps.py** - Django app configuration

## Getting Started

### Prerequisites
- Python 3.12+ (check with `python --version`)
- Docker (for PostgreSQL)
- [uv](https://github.com/astral-sh/uv) package manager

### Initial Setup

1. **Install uv** (if not already installed)
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Set up environment variables**

   Create `.env` file in project root:
   ```bash
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   DATABASE_URL=postgres://makerdb:makerdb@localhost:5432/makerdb
   ```

   Generate a secret key:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

4. **Start PostgreSQL**
   ```bash
   docker compose up -d
   ```

5. **Run migrations**
   ```bash
   uv run python backend/manage.py migrate
   ```

6. **Create superuser** (optional, for admin access)
   ```bash
   uv run python backend/manage.py createsuperuser
   ```

7. **Start development server**
   ```bash
   uv run uvicorn makerdb.asgi:application --reload --app-dir backend
   ```

   The server will be available at:
   - API: http://localhost:8000/api
   - Admin Panel: http://localhost:8000/cp
   - Health Check: http://localhost:8000/api/health

## Development Workflow

### ASGI Application Architecture

The application uses a hybrid architecture defined in [backend/makerdb/asgi.py](../../backend/makerdb/asgi.py):

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

### FastAPI Router Registration

All routers are registered in [backend/makerdb/api.py](../../backend/makerdb/api.py):

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

### Async Pattern with Django ORM

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

## Data Models

### Base Models

All models inherit from base classes in [backend/core/models.py](../../backend/core/models.py):

#### TimeStampedModel
```python
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
```

#### GlobalOpsBase
```python
class GlobalOpsBase(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tags = models.JSONField(default=list, blank=True)
    custom_fields = models.JSONField(default=dict, blank=True)

    class Meta:
        abstract = True
```

All main entities (Part, Project, Order, etc.) inherit from `GlobalOpsBase`, providing:
- UUID primary keys
- Timestamps (created_at, updated_at)
- Tags (JSON array of strings)
- Custom fields (JSON object for flexible metadata)

### Django Apps and Models

| App | Models | Description |
|-----|--------|-------------|
| **core** | Company, Attachment | Base models and utilities |
| **parts** | Part, Designator | Component catalog |
| **inventory** | Storage, Lot, Stock | Storage locations and inventory tracking |
| **projects** | Project, BOMItem | Projects and bills of materials |
| **procurement** | Order, Offer | Purchase orders and vendor pricing |

### Model Relationships

```
Company (Manufacturer/Vendor)
    ↓ (1:N)
Part ← (M:N) → Attachment
    ↓ (1:N)
Stock → Storage (Location)
    ↑ (N:1)
Lot

Project
    ↓ (1:N)
BOMItem → Part
```

## API Development

### Creating a New Endpoint

1. **Define Pydantic Schema** (`schemas.py`)

```python
from pydantic import BaseModel, ConfigDict
from uuid import UUID

class PartBase(BaseModel):
    name: str
    description: str | None = None
    manufacturer_id: UUID | None = None

class PartCreate(PartBase):
    pass

class PartUpdate(PartBase):
    name: str | None = None  # Make fields optional for PATCH

class PartSchema(PartBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
```

2. **Create Endpoint** (`router.py`)

```python
from fastapi import APIRouter, HTTPException
from asgiref.sync import sync_to_async
from .models import Part
from .schemas import PartSchema, PartCreate, PartUpdate

router = APIRouter(prefix="/parts", tags=["Parts"])

@router.get("/", response_model=list[PartSchema])
async def list_parts():
    parts = await sync_to_async(list)(Part.objects.all())
    return parts

@router.post("/", response_model=PartSchema, status_code=201)
async def create_part(data: PartCreate):
    @sync_to_async
    def _create():
        part = Part(**data.model_dump())
        part.save()
        return part

    return await _create()

@router.put("/{part_id}", response_model=PartSchema)
async def update_part(part_id: UUID, data: PartUpdate):
    @sync_to_async
    def _update():
        try:
            part = Part.objects.get(id=part_id)
        except Part.DoesNotExist:
            raise ValueError("Part not found")

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(part, field, value)
        part.save()
        return part

    try:
        return await _update()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{part_id}", status_code=204)
async def delete_part(part_id: UUID):
    @sync_to_async
    def _delete():
        try:
            part = Part.objects.get(id=part_id)
            part.delete()
        except Part.DoesNotExist:
            raise ValueError("Part not found")

    try:
        await _delete()
    except ValueError:
        raise HTTPException(status_code=404, detail="Part not found")
```

3. **Register Router** (in `makerdb/api.py`)

```python
from parts.router import router as parts_router

app.include_router(parts_router)
```

### Query Optimization

Use `select_related()` and `prefetch_related()` to avoid N+1 queries:

```python
def _get_part_queryset():
    return (
        Part.objects
        .select_related("manufacturer", "default_storage")
        .prefetch_related("attachments")
        .annotate(total_stock=Sum("stock_entries__quantity"))
    )

@router.get("/")
async def list_parts():
    parts = await sync_to_async(list)(_get_part_queryset())
    return parts
```

### Pagination

```python
from fastapi import Query

@router.get("/")
async def list_parts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    parts = await sync_to_async(list)(
        Part.objects.all()[skip:skip + limit]
    )
    return parts
```

## Testing

### Running Tests

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest backend/tests/test_models.py

# Run with verbose output
uv run pytest -v

# Run with coverage
uv run pytest --cov=backend

# Recreate test database
uv run pytest --create-db
```

### Test Configuration

Tests are configured in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "makerdb.settings"
python_files = ["test_*.py", "*_test.py"]
pythonpath = "backend"
addopts = "--reuse-db"  # Faster tests by reusing database
```

### Writing Tests

#### Model Tests

```python
# backend/tests/test_models.py
import pytest
from parts.models import Part
from core.models import Company

@pytest.mark.django_db
class TestPartModel:
    def test_create_part(self):
        part = Part.objects.create(
            name="Resistor 10k",
            description="1/4W through-hole"
        )
        assert part.id is not None
        assert part.name == "Resistor 10k"

    def test_part_with_manufacturer(self):
        mfr = Company.objects.create(
            name="Yageo",
            is_manufacturer=True
        )
        part = Part.objects.create(
            name="RC0805",
            manufacturer=mfr
        )
        assert part.manufacturer.name == "Yageo"
```

#### API Tests

```python
# backend/tests/test_api.py
import pytest
from httpx import AsyncClient
from asgiref.sync import async_to_sync

@pytest.mark.django_db
@pytest.mark.asyncio
async def test_list_parts():
    from makerdb.asgi import application

    async with AsyncClient(app=application, base_url="http://test") as client:
        response = await client.get("/api/parts/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

@pytest.mark.django_db
@pytest.mark.asyncio
async def test_create_part():
    from makerdb.asgi import application

    async with AsyncClient(app=application, base_url="http://test") as client:
        data = {"name": "Test Part", "description": "Test"}
        response = await client.post("/api/parts/", json=data)
        assert response.status_code == 201
        assert response.json()["name"] == "Test Part"
```

### Fixtures

Create reusable test data in `tests/conftest.py`:

```python
import pytest
from core.models import Company
from parts.models import Part

@pytest.fixture
def manufacturer():
    return Company.objects.create(
        name="Test Manufacturer",
        is_manufacturer=True
    )

@pytest.fixture
def sample_part(manufacturer):
    return Part.objects.create(
        name="Sample Part",
        manufacturer=manufacturer
    )
```

## Database Management

### Migrations

```bash
# Create migrations after model changes
uv run python backend/manage.py makemigrations

# Apply migrations
uv run python backend/manage.py migrate

# Show migration status
uv run python backend/manage.py showmigrations

# Rollback migration
uv run python backend/manage.py migrate <app_name> <migration_name>
```

### Django Shell

```bash
# Interactive Python shell with Django context
uv run python backend/manage.py shell

# Example shell usage
>>> from parts.models import Part
>>> Part.objects.count()
42
>>> part = Part.objects.first()
>>> part.name
'Resistor 10k'
```

### Database Utilities

```bash
# Dump data to JSON
uv run python backend/manage.py dumpdata parts.Part --indent 2 > parts.json

# Load data from JSON
uv run python backend/manage.py loaddata parts.json

# Reset database (dangerous!)
uv run python backend/manage.py flush
```

## Coding Conventions

### Python Style

- **Line length**: 120 characters (configured in `pyproject.toml`)
- **Type hints**: Use modern syntax (`list[str]` not `List[str]`)
- **Imports**: Organized by ruff (stdlib, third-party, local)
- **Docstrings**: Use for public APIs and complex logic

### Django Models

```python
from django.db import models
from core.models import GlobalOpsBase

class Part(GlobalOpsBase):
    """
    Represents a physical component in the inventory.
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    manufacturer = models.ForeignKey(
        "core.Company",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="parts"
    )

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self) -> str:
        return self.name
```

### Pydantic Schemas

```python
from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import datetime

class PartSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    description: str | None = None
    manufacturer_id: UUID | None = None
    created_at: datetime
    updated_at: datetime

    # Computed fields
    total_stock: int = Field(default=0, description="Total quantity in stock")
```

### Error Handling

```python
from fastapi import HTTPException

@router.get("/{part_id}")
async def get_part(part_id: UUID):
    @sync_to_async
    def _get():
        try:
            return Part.objects.get(id=part_id)
        except Part.DoesNotExist:
            raise ValueError("Part not found")

    try:
        return await _get()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
```

### Async Patterns

```python
# DO: Wrap Django ORM in sync_to_async
@sync_to_async
def _get_parts():
    return list(Part.objects.all())

parts = await _get_parts()

# DON'T: Direct ORM calls in async context
# This will fail!
parts = await Part.objects.all()  # ❌
```

## Common Tasks

### Adding a New Model

1. **Define model** in `models.py`:
   ```python
   class NewModel(GlobalOpsBase):
       name = models.CharField(max_length=255)
   ```

2. **Create migration**:
   ```bash
   uv run python backend/manage.py makemigrations
   ```

3. **Apply migration**:
   ```bash
   uv run python backend/manage.py migrate
   ```

4. **Create Pydantic schemas** in `schemas.py`

5. **Create API endpoints** in `router.py`

6. **Register router** in `makerdb/api.py`

7. **Add admin configuration** in `admin.py` (optional)

### Adding a New Django App

```bash
# Create app
uv run python backend/manage.py startapp newapp

# Add to INSTALLED_APPS in settings.py
INSTALLED_APPS = [
    # ...
    "newapp",
]
```

### Debugging

```python
# Use Python debugger
import pdb; pdb.set_trace()

# Or breakpoint() (Python 3.7+)
breakpoint()

# Print SQL queries
from django.db import connection
print(connection.queries)
```

### Code Quality

```bash
# Lint code
uv run ruff check backend

# Format code
uv run ruff format backend

# Fix auto-fixable issues
uv run ruff check backend --fix
```

---

For more information:
- [Django Documentation](https://docs.djangoproject.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [pytest Documentation](https://docs.pytest.org/)
