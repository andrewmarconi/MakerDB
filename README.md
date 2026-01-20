# MakerDB

![MakerDB Header](docs/media/makerdb-header.jpg)

A single-tenant inventory and parts management system designed for hardware makers, electronics engineers, and small manufacturing teams. MakerDB helps you track parts, manage stock levels, organize storage locations, plan projects with BOMs, and handle procurement.

## Features

- **Parts Management**: Comprehensive component catalog with manufacturer information, datasheets, and custom fields
- **Inventory Tracking**: Real-time stock levels across multiple storage locations with lot tracking
- **Storage Organization**: Hierarchical storage location system with occupancy tracking
- **Project BOMs**: Bill of Materials management with parametric search and part matching
- **Procurement**: Purchase order tracking with vendor offers and pricing history
- **Rich Attachments**: Support for datasheets, images, CAD files, and documents
- **Flexible Metadata**: Custom tags and fields on all major entities
- **Modern UI**: Responsive interface built with Nuxt UI and Tailwind CSS

## Tech Stack

### Backend
- **Django 6.0.1** - ORM, admin panel, and migrations
- **FastAPI** - High-performance REST API
- **PostgreSQL 17** - Primary database
- **Pydantic** - Request/response validation

### Frontend
- **Nuxt 4** - Vue 3 framework with server-side rendering
- **Nuxt UI v4** - Component library built on Tailwind CSS 4
- **Vitest** - Unit and integration testing

The application uses a hybrid architecture where FastAPI is mounted at `/api` within Django's ASGI application, enabling the best of both frameworks while sharing authentication and database access.

## Quick Start

### Prerequisites
- Python 3.12+
- Node.js 18+
- Docker (for PostgreSQL)
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd MakerDB
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

   Required variables:
   - `SECRET_KEY` - Django secret key
   - `DEBUG` - Set to `True` for development
   - `DATABASE_URL` - PostgreSQL connection string (default: `postgres://makerdb:makerdb@localhost:5432/makerdb`)

3. **Start PostgreSQL**
   ```bash
   docker compose up -d
   ```

4. **Set up backend**
   ```bash
   uv sync
   uv run python backend/manage.py migrate
   uv run uvicorn makerdb.asgi:application --reload --app-dir backend
   ```

   The backend will be available at:
   - API: http://localhost:8000/api
   - Admin Panel: http://localhost:8000/cp

5. **Set up frontend** (in a new terminal)
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

   The frontend will be available at http://localhost:3000

Alternatively, run both backend and frontend together from the frontend directory:
```bash
cd frontend
npm run dev:all
```

## Development

### Running Tests

**Backend:**
```bash
uv run pytest                                  # Run all tests
uv run pytest backend/tests/test_file.py       # Run specific test file
uv run pytest --create-db                      # Recreate test database
```

**Frontend:**
```bash
cd frontend
npm test              # Run all tests
npm run test:unit     # Unit tests only
npm run test:nuxt     # Nuxt integration tests
```

### Code Quality

**Backend:**
```bash
uv run ruff check backend     # Lint
uv run ruff format backend    # Format
```

**Frontend:**
ESLint is configured via Nuxt ESLint module.

## Project Structure

```
MakerDB/
├── backend/
│   ├── makerdb/          # Django project settings
│   │   ├── asgi.py       # ASGI app (mounts FastAPI + Django)
│   │   ├── api.py        # FastAPI router registration
│   │   └── settings.py   # Django settings
│   ├── core/             # Base models (Company, Attachment)
│   ├── parts/            # Parts management
│   ├── inventory/        # Stock and storage locations
│   ├── projects/         # Projects and BOMs
│   └── procurement/      # Orders and vendor offers
├── frontend/
│   └── app/              # Nuxt source directory
│       ├── components/
│       ├── pages/
│       └── layouts/
├── docs/                 # Extended documentation (see below)
├── docker-compose.yml    # PostgreSQL service
└── pyproject.toml        # Python dependencies (uv)
```

Each Django app follows the pattern:
- `models.py` - Django ORM models
- `schemas.py` - Pydantic schemas for API validation
- `router.py` - FastAPI CRUD endpoints

## Documentation

### Developer Documentation

Comprehensive guides for contributing to MakerDB can be found in the [`docs/developer/`](docs/developer/) directory:

- **[Developer Guide](docs/developer/index.md)** - Start here for an overview of the architecture and development workflow
- **[Frontend Development](docs/developer/frontend/)** - Vue.js, Nuxt 4, TypeScript, and UI development
  - [Getting Started](docs/developer/frontend/getting-started.md)
  - [Technology Stack](docs/developer/frontend/technology-stack.md)
  - [Component Development](docs/developer/frontend/component-development.md)
  - [Testing](docs/developer/frontend/testing.md)
- **[Backend Development](docs/developer/backend/)** - Django, FastAPI, and API development
  - [Getting Started](docs/developer/backend/getting-started.md)
  - [Technology Stack](docs/developer/backend/technology-stack.md)
  - [API Development](docs/developer/backend/api-development.md)
  - [Testing](docs/developer/backend/testing.md)
- **[Contributing Guidelines](docs/developer/contributing/)** - How to contribute to the project
  - [Getting Started](docs/developer/contributing/getting-started.md)
  - [Development Workflow](docs/developer/contributing/development-workflow.md)
  - [Pull Request Process](docs/developer/contributing/pull-request-process.md)
  - [Code of Conduct](docs/developer/contributing/code-of-conduct.md)

### Additional Documentation

- **[CLAUDE.md](CLAUDE.md)** - Quick reference for AI-assisted development
- **Architecture Overview** - System design and data model (coming soon)
- **API Reference** - REST API endpoints and schemas (coming soon)
- **Deployment Guide** - Production deployment instructions (coming soon)
- **User Guide** - End-user documentation (coming soon)

## Contributing

We welcome contributions from developers of all skill levels! Whether you're interested in frontend, backend, or full-stack development, there's a place for you.

**To get started:**

1. Read the [Developer Guide](docs/developer/index.md) for an overview
2. Check out specific guides:
   - [Frontend Development](docs/developer/frontend/) - For UI/UX work
   - [Backend Development](docs/developer/backend/) - For API and database work
3. Review the [Contributing Guidelines](docs/developer/contributing/)
4. Find an issue labeled `good first issue` to work on

For AI-assisted development, see [CLAUDE.md](CLAUDE.md) for quick reference commands and conventions.

## Database Admin

Access the Django admin panel at http://localhost:8000/cp (Jazzmin theme) to:
- Manage data directly
- View model relationships
- Perform bulk operations

## Support

For questions, issues, or feature requests, please [open an issue](../../issues).

---

Built with ❤️ for the maker community
