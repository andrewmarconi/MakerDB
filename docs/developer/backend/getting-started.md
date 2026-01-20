# Getting Started

## Prerequisites
- Python 3.12+ (check with `python --version`)
- Docker (for PostgreSQL)
- [uv](https://github.com/astral-sh/uv) package manager

## Initial Setup

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
