# Project Structure

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

## Django App Pattern

Each Django app follows a consistent structure:

1. **models.py** - Django ORM models
2. **schemas.py** - Pydantic schemas for API validation
3. **router.py** - FastAPI router with CRUD endpoints
4. **admin.py** - Django admin configuration
5. **apps.py** - Django app configuration
