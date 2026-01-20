# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MakerDB is a single-tenant inventory and parts management system for hardware makers. It manages parts, stock/inventory, storage locations, projects/BOMs, and procurement (orders, vendor offers).

## Development Commands

### Backend (Django + FastAPI)

```bash
# Start PostgreSQL database (required first)
docker compose up -d

# Install/sync Python dependencies
uv sync

# Run Django migrations
uv run python backend/manage.py migrate

# Start development server (ASGI - serves both Django and FastAPI)
uv run uvicorn makerdb.asgi:application --reload --app-dir backend

# Run backend tests (uses --reuse-db by default)
uv run pytest

# Run a single test file
uv run pytest backend/tests/test_domain_phase2.py

# Recreate test database
uv run pytest --create-db

# Lint/format
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

# Run unit tests only
npm run test:unit

# Run Nuxt integration tests
npm run test:nuxt

# Build for production
npm run build
```

## Architecture

### Backend Stack
- **Django 6.0.1**: ORM and admin panel (Jazzmin theme at `/cp/`)
- **FastAPI**: REST API mounted at `/api` within Django's ASGI app
- **PostgreSQL 17**: Database via Docker Compose

The ASGI application ([backend/makerdb/asgi.py](backend/makerdb/asgi.py)) mounts FastAPI at `/api` and Django at root, sharing the same process and authentication sessions.

### Frontend Stack
- **Nuxt 4** with Vue 3 (srcDir: `app/`)
- **Nuxt UI v4** with Tailwind CSS 4
- **Vitest** with two test projects: `unit` (node) and `nuxt` (happy-dom)

The frontend proxies `/db/**` requests to `http://localhost:8000/api/**` via Nitro route rules.

### Django Apps

| App | Purpose |
|-----|---------|
| `core` | Base models (`TimeStampedModel`, `GlobalOpsBase`), `Company`, `Attachment` |
| `parts` | `Part` model - component catalog with manufacturer info, stock thresholds |
| `inventory` | `Storage` (locations), `Lot` (batches), `Stock` (part quantities at locations) |
| `projects` | `Project` and `BOMItem` - bill of materials management |
| `procurement` | `Order` (purchase orders) and `Offer` (vendor pricing) |

All main entities inherit from `GlobalOpsBase` which provides UUID primary keys, `tags` (JSON array), `custom_fields` (JSON object), and timestamps.

### FastAPI Routing Pattern

Each Django app contains:
- `models.py` - Django ORM models
- `schemas.py` - Pydantic schemas for API request/response validation
- `router.py` - FastAPI router with CRUD endpoints

All routers are registered in [backend/makerdb/api.py](backend/makerdb/api.py). FastAPI routes use `sync_to_async` decorator to call Django ORM operations asynchronously.

### Key Conventions

- **Package manager**: `uv` only (never pip/poetry/pipenv)
- **Python**: 3.12+ with modern type hints (`list[str]` not `List[str]`)
- **Async**: FastAPI routes use `sync_to_async` from `asgiref.sync` to wrap Django ORM calls
- **Config**: Use `django-environ` with `.env` file at project root
- **Linting**: `ruff` only (replaces flake8/isort/black)
- **Testing**: `pytest` with `pytest-django` (not unittest)

### Environment Variables

Required in `.env`:
- `SECRET_KEY` - Django secret key
- `DEBUG` - Boolean
- `DATABASE_URL` - PostgreSQL connection string (e.g., `postgres://makerdb:makerdb@localhost:5432/makerdb`)
