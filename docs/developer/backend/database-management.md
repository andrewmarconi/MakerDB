# Database Management

## Migrations

```bash
# Create migrations after model changes
uv run python backend/manage.py makemigrations

# Apply migrations
uv run python backend/manage.py migrate

# Show migration status
uv run python backend/manage.py showmigrations

# Rollback migration
uv run python backend/manage.py migrate <app_name> <migration_name>
```

## Django Shell

```bash
# Interactive Python shell with Django context
uv run python backend/manage.py shell

# Example shell usage
>>> from parts.models import Part
>>> Part.objects.count()
42
>>> part = Part.objects.first()
>>> part.name
'Resistor 10k'
```

## Database Utilities

```bash
# Dump data to JSON
uv run python backend/manage.py dumpdata parts.Part --indent 2 > parts.json

# Load data from JSON
uv run python backend/manage.py loaddata parts.json

# Reset database (dangerous!)
uv run python backend/manage.py flush
```
