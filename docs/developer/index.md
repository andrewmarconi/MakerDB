# Developer Documentation

Welcome to the MakerDB developer documentation! This guide will help you get started contributing to MakerDB, whether you're working on the frontend, backend, or both.

## Quick Links

- **[Frontend Development Guide](frontend/index.md)** - Vue.js, Nuxt 4, and UI development
- **[Backend Development Guide](backend/index.md)** - Django, FastAPI, and API development
- **[Contributing Guidelines](contributing/index.md)** - How to contribute to the project
- **[Project README](../../README.md)** - Project overview and quick start

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
- [Development Areas](#development-areas)
- [Common Workflows](#common-workflows)
- [Resources](#resources)

## Architecture Overview

MakerDB uses a modern, full-stack architecture with clear separation between frontend and backend:

```
┌─────────────────────────────────────────────────────┐
│                   Frontend (Nuxt 4)                  │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────┐ │
│   │   Pages      │  │  Components  │  │  Assets  │ │
│   │ (Routing)    │  │  (Nuxt UI)   │  │ (CSS)    │ │
│   └──────────────┘  └──────────────┘  └──────────┘ │
│                         ↓                            │
│                  Vue 3 + TypeScript                  │
│                  Tailwind CSS 4                      │
└─────────────────────────────────────────────────────┘
                         ↓ HTTP
              /db/** → /api/** (Proxy)
                         ↓
┌─────────────────────────────────────────────────────┐
│              Backend (Django + FastAPI)              │
│   ┌────────────────────────────────────────┐        │
│   │         ASGI Application               │        │
│   │  ┌──────────────┐  ┌────────────────┐ │        │
│   │  │   FastAPI    │  │     Django     │ │        │
│   │  │  /api/*      │  │    /cp/*       │ │        │
│   │  │   (API)      │  │   (Admin)      │ │        │
│   │  └──────────────┘  └────────────────┘ │        │
│   └────────────────────────────────────────┘        │
│                         ↓                            │
│                    Django ORM                        │
│                         ↓                            │
│                  PostgreSQL 17                       │
└─────────────────────────────────────────────────────┘
```

### Key Architectural Decisions

1. **Hybrid Backend** - Django provides ORM, migrations, and admin; FastAPI provides high-performance async API endpoints
2. **Single Process** - Both frameworks run in one ASGI process, sharing database and authentication
3. **File-based Routing** - Frontend uses Nuxt's automatic routing based on file structure
4. **Component Library** - Nuxt UI v4 provides pre-built, accessible components
5. **Type Safety** - TypeScript on frontend, Pydantic schemas on backend

## Technology Stack

### Frontend Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| **Nuxt 4** | ^4.2.2 | Vue 3 meta-framework with SSR |
| **Vue 3** | ^3.5.26 | Reactive UI framework |
| **Nuxt UI** | ^4.3.0 | Component library |
| **Tailwind CSS** | ^4.1.18 | Utility-first CSS framework |
| **TypeScript** | ^5.9.3 | Type-safe JavaScript |
| **Vitest** | ^3.2.4 | Unit testing framework |

### Backend Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| **Django** | 6.0.1 | ORM, migrations, admin |
| **FastAPI** | ^0.128.0 | Async REST API framework |
| **PostgreSQL** | 17 | Primary database |
| **Pydantic** | (via FastAPI) | Data validation |
| **pytest** | ^9.0.2 | Testing framework |
| **Ruff** | ^0.14.13 | Linting and formatting |

### Development Tools

| Tool | Purpose |
|------|---------|
| **uv** | Python package manager |
| **npm** | Node.js package manager |
| **Docker** | PostgreSQL containerization |
| **Git** | Version control |
| **GitHub** | Code hosting and collaboration |

## Getting Started

### First-Time Setup

1. **Prerequisites**

   Ensure you have installed:
   - Python 3.12+ ([python.org](https://www.python.org/))
   - Node.js 18+ ([nodejs.org](https://nodejs.org/))
   - Docker ([docker.com](https://www.docker.com/))
   - uv package manager ([docs.astral.sh/uv](https://docs.astral.sh/uv/))
   - Git ([git-scm.com](https://git-scm.com/))

2. **Clone the Repository**

   ```bash
   git clone https://github.com/andrewmarconi/MakerDB.git
   cd MakerDB
   ```

3. **Backend Setup**

   ```bash
   # Install dependencies
   uv sync

   # Set up environment variables
   cp .env.example .env
   # Edit .env with your configuration

   # Start PostgreSQL
   docker compose up -d

   # Run migrations
   uv run python backend/manage.py migrate

   # Create superuser (optional)
   uv run python backend/manage.py createsuperuser

   # Start development server
   uv run uvicorn makerdb.asgi:application --reload --app-dir backend
   ```

   Backend will be available at:
   - API: http://localhost:8000/api
   - Admin: http://localhost:8000/cp

4. **Frontend Setup**

   ```bash
   cd frontend

   # Install dependencies
   npm install

   # Start development server
   npm run dev
   ```

   Frontend will be available at http://localhost:3000

5. **Verify Setup**

   ```bash
   # Backend tests
   uv run pytest

   # Frontend tests
   cd frontend
   npm test
   ```

### Quick Start (Both Services)

Run both backend and frontend together:

```bash
cd frontend
npm run dev:all
```

This starts both services with a single command using concurrently.

## Development Areas

### Where to Contribute

Depending on your interests and skills, you can contribute to different areas:

#### 1. Frontend Development
**Skills**: Vue.js, TypeScript, CSS/Tailwind
**See**: [Frontend Development Guide](frontend/index.md)

**Common tasks**:
- Building UI components
- Creating new pages and routes
- Implementing forms and validation
- Improving responsiveness and accessibility
- Writing frontend tests

#### 2. Backend Development
**Skills**: Python, Django, FastAPI, SQL
**See**: [Backend Development Guide](backend/index.md)

**Common tasks**:
- Adding new API endpoints
- Creating/modifying Django models
- Writing database migrations
- Implementing business logic
- Writing backend tests

#### 3. Full-Stack Features
**Skills**: Both frontend and backend
**See**: Both guides above

**Common tasks**:
- End-to-end feature implementation
- API integration
- Data flow optimization
- Performance improvements

#### 4. Testing & Quality
**Skills**: Testing frameworks, debugging
**See**: [Contributing Guidelines](contributing/index.md)

**Common tasks**:
- Writing unit tests
- Writing integration tests
- Improving test coverage
- Finding and reporting bugs

#### 5. Documentation
**Skills**: Technical writing, markdown
**See**: [Contributing Guidelines](contributing/index.md)

**Common tasks**:
- Improving developer docs
- Writing user guides
- Creating tutorials
- Updating API documentation

## Common Workflows

### Adding a New Feature

1. **Understand the requirements**
   - Check the GitHub issue
   - Discuss with maintainers if needed

2. **Plan your approach**
   - Identify affected files
   - Consider data model changes
   - Think about testing strategy

3. **Backend implementation** (if needed)
   - Update/create Django models
   - Create database migration
   - Write Pydantic schemas
   - Implement API endpoints
   - Write backend tests

4. **Frontend implementation** (if needed)
   - Create/update components
   - Add pages/routes
   - Integrate with API
   - Write frontend tests

5. **Testing**
   - Run all tests
   - Manual testing
   - Check code quality

6. **Documentation**
   - Update relevant docs
   - Add code comments
   - Update changelog (if applicable)

7. **Submit PR**
   - Follow PR template
   - Link related issues
   - Request review

### Fixing a Bug

1. **Reproduce the bug**
   - Follow reproduction steps
   - Understand the root cause

2. **Write a failing test**
   - Create a test that demonstrates the bug
   - This prevents regression

3. **Fix the bug**
   - Make minimal changes
   - Follow coding conventions

4. **Verify the fix**
   - Test passes
   - Manual testing
   - No side effects

5. **Submit PR**
   - Reference the bug issue
   - Explain the fix

### Working on Documentation

1. **Identify what needs documenting**
   - New features
   - Unclear existing docs
   - Missing examples

2. **Write clear, concise content**
   - Use examples
   - Be specific
   - Think about the audience

3. **Review and test**
   - Check for typos
   - Verify code examples work
   - Ensure links work

4. **Submit PR**
   - Use `docs/` prefix in branch name
   - Explain what's being documented

## Code Organization

### Backend Structure

```
backend/
├── makerdb/              # Django project
│   ├── settings.py      # Configuration
│   ├── asgi.py         # ASGI app (FastAPI + Django)
│   └── api.py          # FastAPI router registration
├── core/                # Base models
├── parts/               # Parts management
├── inventory/           # Inventory & storage
├── projects/            # Projects & BOMs
├── procurement/         # Orders & offers
└── tests/              # Test suite
```

Each app contains:
- `models.py` - Django ORM models
- `schemas.py` - Pydantic schemas
- `router.py` - FastAPI endpoints
- `admin.py` - Django admin config

### Frontend Structure

```
frontend/app/
├── components/          # Vue components
│   ├── Dashboard/      # Dashboard widgets
│   ├── Files/          # File management
│   ├── Search/         # Search components
│   └── *.vue           # Global components
├── pages/              # File-based routing
│   ├── index.vue      # Dashboard (/)
│   ├── inventory/     # Inventory pages
│   ├── projects/      # Project pages
│   └── ...
├── layouts/            # Layout components
├── composables/        # Vue composables
├── utils/             # Utility functions
└── assets/            # CSS and static files
```

## Development Best Practices

### General Principles

1. **Keep it simple** - Don't over-engineer solutions
2. **Write tests** - Test your code before submitting
3. **Follow conventions** - Consistency matters
4. **Document your code** - Especially complex logic
5. **Ask questions** - Better to ask than to assume

### Code Quality

- Run linters before committing
- Write meaningful commit messages
- Keep functions/components focused
- Use descriptive variable names
- Add comments for complex logic

### Performance

- Optimize database queries (avoid N+1)
- Use pagination for large datasets
- Lazy load when appropriate
- Profile before optimizing

### Security

- Never commit secrets
- Validate all user input
- Use parameterized queries
- Follow framework security guidelines

## Resources

### Official Documentation

- [Django Documentation](https://docs.djangoproject.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Nuxt 4 Documentation](https://nuxt.com/)
- [Vue 3 Documentation](https://vuejs.org/)
- [Nuxt UI Documentation](https://ui.nuxt.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [pytest Documentation](https://docs.pytest.org/)
- [Vitest Documentation](https://vitest.dev/)

### Learning Resources

#### Backend
- [Django for Beginners](https://djangoforbeginners.com/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Real Python](https://realpython.com/)

#### Frontend
- [Vue.js Guide](https://vuejs.org/guide/)
- [Nuxt Documentation](https://nuxt.com/docs)
- [Tailwind CSS Course](https://tailwindcss.com/docs)

### Community

- GitHub Issues - Bug reports and feature requests
- GitHub Discussions - Questions and community discussion
- Pull Requests - Code contributions and reviews

## Getting Help

### Common Questions

**Q: I'm new to Django/Vue. Where should I start?**
A: Start with small tasks like documentation improvements or bug fixes. Read the relevant development guide ([Frontend](frontend/index.md) or [Backend](backend/index.md)) and explore the codebase.

**Q: How do I run tests?**
A: Backend: `uv run pytest`, Frontend: `cd frontend && npm test`

**Q: My tests are failing. What should I do?**
A: Make sure you've run migrations (`uv run python backend/manage.py migrate`) and that your database is running (`docker compose up -d`).

**Q: How do I add a new dependency?**
A: Backend: `uv add package-name`, Frontend: `npm install package-name`. Commit the updated lock files.

**Q: Where do I ask questions?**
A: Open a GitHub issue with the "question" label or start a GitHub Discussion.

### Troubleshooting

**Backend won't start**
- Check that PostgreSQL is running: `docker ps`
- Verify environment variables in `.env`
- Run migrations: `uv run python backend/manage.py migrate`

**Frontend won't start**
- Delete `node_modules` and reinstall: `rm -rf node_modules && npm install`
- Check Node.js version: `node --version` (should be 18+)

**Tests failing**
- Run `uv run pytest --create-db` to recreate test database
- Make sure all dependencies are installed: `uv sync`

**Database issues**
- Reset database: `docker compose down -v && docker compose up -d`
- Run migrations: `uv run python backend/manage.py migrate`

## Next Steps

1. **Read the guides**
   - [Frontend Development Guide](frontend/index.md) for UI work
   - [Backend Development Guide](backend/index.md) for API work
   - [Contributing Guidelines](contributing/index.md) for workflow

2. **Set up your environment**
   - Follow the "Getting Started" section above
   - Verify everything works with tests

3. **Find an issue to work on**
   - Look for "good first issue" label
   - Comment on the issue to claim it
   - Ask questions if anything is unclear

4. **Make your first contribution**
   - Create a branch
   - Make your changes
   - Submit a pull request

5. **Join the community**
   - Review others' pull requests
   - Help answer questions
   - Share your knowledge

---

**Welcome to the MakerDB community!**

If you have questions or suggestions for improving this documentation, please open an issue or pull request.
