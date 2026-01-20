# Technology Stack

## Core Frameworks
- **Django 6.0.1** - ORM, migrations, admin panel, authentication
- **FastAPI** (`^0.128.0`) - Modern async web framework for APIs
- **Uvicorn** (`^0.40.0`) - ASGI server with auto-reload

## Database
- **PostgreSQL 17** - Primary database (via Docker Compose)
- **psycopg[binary]** (`^3.3.2`) - PostgreSQL adapter for Python

## Configuration & Utilities
- **django-environ** (`^0.12.0`) - Environment variable management
- **django-jazzmin** (`^3.0.1`) - Modern Django admin theme
- **python-multipart** (`^0.0.20`) - Multipart form data parsing
- **whitenoise** (`^6.8.0`) - Static file serving

## Development Tools
- **pytest** (`^9.0.2`) - Testing framework
- **pytest-django** (`^4.11.1`) - Django plugin for pytest
- **ruff** (`^0.14.13`) - Fast Python linter and formatter

## Package Manager
- **uv** - Modern, fast Python package manager (replaces pip/poetry/pipenv)
