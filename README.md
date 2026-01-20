# MakerDB

MakerDB is a single-tenant inventory and parts management system.

## Documentation
*   [Development Standards](docs/development_standards.md)
*   [Schema Design](docs/django_schema_design.py)

## Development

### Support Services
```bash
docker compose up -d
```

### Backend Service
```bash
cd backend
uv sync
uv run python manage.py migrate # If needed
cd /Users/andrew/Develop/MakerDB && .venv/bin/python -m uvicorn makerdb.asgi:application --app-dir backend

```

### Frontend Services
```bash
cd frontend
npm install
npm run dev
```

