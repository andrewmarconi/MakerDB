# AGENTS.md

This file provides guidance for agentic coding agents operating in this repository.

## Build/Lint/Test Commands

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

# Run all backend tests
uv run pytest

# Run a single test file
uv run pytest backend/tests/test_domain_phase2.py

# Run a single test
uv run pytest backend/tests/test_domain_phase2.py::test_project_creation

# Lint
uv run ruff check backend

# Format
uv run ruff format backend
```

### Frontend (Nuxt 4)

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev

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

**Imports**: Standard library first, then third-party, then local. Use absolute imports from the project root.

**Type Hints**: Use modern syntax (`list[str]`, `dict[str, int]` not `List[str]`, `Dict[str, int]`). Always annotate function return types.

**Naming**:
- `snake_case` for functions, variables, and module names
- `PascalCase` for classes and exceptions
- `UPPER_SNAKE_CASE` for constants
- Single leading underscore for "private" internal methods

**Formatting**: Line length 120 characters. Let ruff handle formatting (no manual formatting).

**Docstrings**: Use for all public classes and functions. Prefer concise one-line summaries for simple functions.

**Error Handling**:
- Use specific exceptions (not bare `except:`)
- Let exceptions propagate in FastAPI routes; rely on global exception handlers
- Validate inputs early with pydantic models in FastAPI endpoints

**Async**: Prefer async ORM calls (`alib`) in FastAPI routes for database operations.

**Django Models**:
- Abstract base classes: `TimeStampedModel`, `GlobalOpsBase`
- Primary keys: UUID via `models.UUIDField(default=uuid.uuid4, editable=False)`
- Common fields: `tags` (JSON array), `custom_fields` (JSON dict) via `models.JSONField`
- Use `related_name` on ForeignKey fields
- Always define `__str__` methods

**Testing**: Use `pytest` with `pytest-django`. Mark tests with `@pytest.mark.django_db`. Place tests in `backend/tests/`.

### Vue/TypeScript (Frontend)

**Composition API**: Use `<script setup>` with Composition API.

**TypeScript**: Enable strict mode. Define interfaces for complex props.

**Component Structure**:
- Imports at top (Nuxt auto-imports: `useRoute`, `useAsyncData`, etc.)
- `definePageMeta()` for page metadata
- Component props with TypeScript types
- Use Nuxt UI components (`UCard`, `UButton`, `UIcon`, etc.)

**Naming**: PascalCase for components (`BOMTable.vue`), camelCase for variables/functions.

**Styling**: Tailwind CSS classes. Use Nuxt UI color/size props.

**Tests**: Vitest with two projects: `unit` (node environment) and `nuxt` (happy-dom). Place tests in `frontend/test/`.

### General

**Package Managers**: `uv` for Python only, `npm` for Node.js only. Never pip/poetry/pipenv or yarn/pnpm.

**Configuration**: Environment variables via `django-environ` in `.env` file at project root.

**Linting**: Ruff for Python, ESLint for JavaScript/TypeScript.

**Dependencies**: Add to `pyproject.toml` or `package.json` directly (no separate lockfiles).

**Git**: Create meaningful commit messages. Don't commit `.env` files or generated files.
