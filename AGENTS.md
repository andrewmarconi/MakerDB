# AGENTS.md

This file provides guidance for agentic coding agents operating in this repository.

## Project Overview

MakerDB is a single-tenant inventory and parts management system for hardware makers. Stack: Django 6.0.1 + FastAPI (ASGI), PostgreSQL 17, Nuxt 4 + Vue 3, Tailwind CSS 4. Entities: Parts, Stock, Storage, Lots, Projects/BOMs, Orders, Offers, Companies, Attachments.

## Build/Lint/Test Commands

### Backend (Django + FastAPI)

```bash
# Start PostgreSQL (required first)
docker compose up -d

# Install/sync Python dependencies
uv sync

# Run Django migrations
uv run python backend/manage.py migrate

# Start dev server (serves Django at /cp and FastAPI at /api)
uv run uvicorn makerdb.asgi:application --reload --app-dir backend

# Run all backend tests (uses --reuse-db by default for speed)
uv run pytest

# Run a single test file
uv run pytest backend/tests/test_domain_phase2.py

# Run a single test
uv run pytest backend/tests/test_domain_phase2.py::test_project_creation

# Recreate test database fresh
uv run pytest --create-db

# Lint and format
uv run ruff check backend
uv run ruff format backend
```

### Frontend (Nuxt 4)

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev

# Run both backend and frontend together
npm run dev:all

# Run all tests
npm test

# Run unit tests only (node environment)
npm run test:unit

# Run Nuxt integration tests (happy-dom)
npm run test:nuxt

# Build for production
npm run build

# Watch mode for tests
npm run test:watch
```

## Code Style Guidelines

### Python (Backend)

**Imports**: Standard library first, then third-party, then local. Use absolute imports from project root.

```python
from typing import List
from uuid import UUID
from fastapi import APIRouter, HTTPException
from asgiref.sync import sync_to_async
from parts.models import Part
```

**Type Hints**: Use modern syntax (`list[str]`, `dict[str, int]` not `List[str]`, `Dict[str, int]`). Always annotate function return types.

**Naming**:
- `snake_case` for functions, variables, and module names
- `PascalCase` for classes and exceptions
- `UPPER_SNAKE_CASE` for constants
- Single leading underscore for "private" internal methods

**Formatting**: Line length 120 characters. Let ruff handle formatting (no manual formatting).

**Docstrings**: Use for all public classes and functions. Prefer concise one-line summaries.

**Error Handling**:
- Use specific exceptions (not bare `except:`)
- Use `HTTPException` in FastAPI routes with appropriate status codes
- Validate inputs early with pydantic models
- Let exceptions propagate; rely on global exception handlers

```python
@router.get("/items/{item_id}")
async def get_item(item_id: UUID):
    try:
        item = await sync_to_async(Item.objects.get)(id=item_id)
        return item
    except Item.DoesNotExist:
        raise HTTPException(status_code=404, detail="Item not found")
```

**Async Pattern**: FastAPI routes use `sync_to_async` to wrap Django ORM calls:

```python
@router.get("/items")
async def list_items():
    @sync_to_async
    def _list():
        return list(Item.objects.all()[0:100])
    return await _list()
```

**Django Models**:
- Abstract base classes: `TimeStampedModel`, `GlobalOpsBase`
- Primary keys: UUID via `models.UUIDField(default=uuid.uuid4, editable=False)`
- Common fields: `tags` (JSON array), `custom_fields` (JSON dict) via `models.JSONField`
- Use `related_name` on ForeignKey fields
- Always define `__str__` methods

**Pydantic Schemas**:
- Use `BaseModel` with `ConfigDict(from_attributes=True)` for ORM integration
- Use `Field(default_factory=list)` for mutable defaults
- Separate read (`CompanySchema`) and write (`CompanyCreate`) schemas
- Inherit from common bases like `GlobalOpsSchema`

**FastAPI Routing**:
- Each Django app has `router.py` with `APIRouter(prefix="/app", tags=["App"])`
- Register routers in `backend/makerdb/api.py`
- Response models define output structure

**Testing**: Use `pytest` with `pytest-django`. Mark tests with `@pytest.mark.django_db`. Place tests in `backend/tests/`.

### Vue/TypeScript (Frontend)

**Composition API**: Use `<script setup>` with Composition API.

**TypeScript**: Enable strict mode. Define interfaces for complex props. Use `PropType` for array/object props.

**Component Structure**:
- Imports at top (Nuxt auto-imports: `useRoute`, `useAsyncData`, `useApiFetch`, etc.)
- `defineProps()` and `defineEmits()` for component interface
- Composables with `ref`, `computed`, `watch` for reactivity
- Use Nuxt UI components (`UCard`, `UButton`, `UIcon`, `UBadge`, etc.)

**Naming**: PascalCase for components (`BOMTable.vue`), camelCase for variables/functions.

**Styling**: Tailwind CSS classes. Use Nuxt UI color/size props over inline styles.

**API Calls**: Use `useApiFetch('/path')` which proxies `/db/**` to `http://localhost:8000/api/**`.

**Tests**: Vitest with two projects: `unit` (node environment) and `nuxt` (happy-dom). Place tests in `frontend/test/unit/` or `frontend/test/nuxt/`.

### General

**Package Managers**: `uv` for Python only, `npm` for Node.js only. Never pip/poetry/pipenv or yarn/pnpm.

**Configuration**: Environment variables via `django-environ` in `.env` file at project root.

**Linting**: Ruff for Python, ESLint for JavaScript/TypeScript (via @nuxt/eslint).

**Dependencies**: Add to `pyproject.toml` or `package.json` directly (no separate lockfiles).

**Git**: Create meaningful commit messages. Use "Closes #XX" to auto-close issues. Don't commit `.env` files or generated files.

**Django Apps Pattern**: Each app follows: `models.py` (ORM), `schemas.py` (Pydantic), `router.py` (FastAPI routes).

## Project Structure

```
backend/
├── makerdb/          # Django project settings
│   ├── asgi.py       # ASGI app (mounts FastAPI + Django)
│   ├── api.py        # FastAPI router registration
│   └── settings.py   # Django settings
├── core/             # Base models, Company, Attachment
├── parts/            # Parts management
├── inventory/        # Stock, Storage, Lots
├── projects/         # Projects, BOMs
├── procurement/      # Orders, Offers
└── dashboard/        # Dashboard metrics endpoints

frontend/
└── app/
    ├── components/   # Vue components
    ├── pages/        # Nuxt pages
    ├── composables/  # useApiFetch, etc.
    └── layouts/      # Page layouts
```
