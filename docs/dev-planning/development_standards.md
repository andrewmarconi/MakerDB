# Development Standards & Rules

## 1. Technology Stack
*   **Python Version**: 3.12 (Strict requirement)
*   **Core Framework**: Django 6.0.1
*   **API Interface**: FastAPI
*   **Asynchronous Support**: Fully supported via ASGI

## 2. Package Management: `uv`
**CRITICAL RULE**: The `uv` package manager is MANDATORY.
*   **Do not** use `pip` directly.
*   **Do not** use `poetry` or `pipenv`.
*   All dependencies must be managed via `pyproject.toml` using `uv`.

### Common Commands
*   **Initialize Project**: `uv init`
*   **Add Dependency**: `uv add <package>` (e.g., `uv add django==6.0.1`)
*   **Add Dev Dependency**: `uv add --dev <package>`
*   **Sync Environment**: `uv sync`
*   **Run Commands**: `uv run python manage.py runserver`

## 3. Project Structure & Configuration
### Layout
*   **`src/` Directory**: All application code must reside in a `src/` directory at the project root.
    *   Example: `src/manage.py`, `src/makerdb/settings.py`
    *   This keeps the root directory clean (only config files like `pyproject.toml`, `.env`, `docker-compose.yml` reside at root).

### Configuration
*   **`django-environ`**: STRICTLY REQUIRED for handling settings.
*   **`.env` File**: All secrets (DB credentials, API keys, Debug flags) must be loaded from a `.env` file in the project root.
*   **No Hardcoding**: Never commit sensitive values to git.

## 4. Architecture Guidelines
### Single-Tenancy
*   This is a **single-tenant** system.
*   **Do not** implement tenant isolation logic.
*   **Do not** add `tenant_id` foreign keys to models.
*   **Do not** extend the base `User` model for multi-tenancy purposes. Standard Django authentication is sufficient.

### Django + FastAPI Integration
*   Django is the SOURCE OF TRUTH for data models (ORM).
*   **FastAPI Mounting**: FastAPI must be mounted **inside** the Django ASGI application (typically at `/api`).
    *   This allows sharing the same process and, crucially, **Django authentication sessions**.
    *   Do NOT run FastAPI as a separate service on a different port.
*   **Do not** duplicate models in Pydantic if ModelSchema/Django-Ninja style integration can be achieved, but typically keep Pydantic schemas for API validation separate but mapped to Django models.
*   Use Django's async ORM features (`alib`) when accessing data from FastAPI routes.

## 5. Quality Assurance (Linting & Testing)
*   **Linter & Formatter**: `ruff` is mandatory.
    *   It replaces `flake8`, `isort`, and `black`.
    *   Configuration must be defined in `pyproject.toml`.
*   **Testing**: `pytest` (with `pytest-django`) is the required testing framework.
    *   Do not use the standard `unittest` or `django.test.TestCase`.


## 6. Coding Standards
*   **Type Hinting**: Python 3.12+ generic syntax is required (e.g., `list[str]` instead of `List[str]`).
*   **Async**: Prefer asynchronous views and ORM calls where possible to leverage the ASGI stack.

## 7. UI & Admin Interface
*   **Admin Theme**: `django-jazzmin` is required.
*   **Admin URL**: The control panel must be hosted at `/cp/`, not the default `/admin/`.

## 8. Infrastructure & Docker
*   **Database**: PostgreSQL 17.x via Docker Compose.
*   **Services**: Any other backing services (Redis, etc.) must be defined in `docker-compose.yml`.
*   **Development Workflow**:
    *   **Services**: Run in Docker containers.
    *   **Application Code**: Run LOCALLY (on host machine) using `uv`. Do NOT containerize the Django/FastAPI app during development to ensure speed and simplicity (no rebuilds required).
