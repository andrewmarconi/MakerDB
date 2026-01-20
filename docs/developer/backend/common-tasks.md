# Common Tasks

## Adding a New Model

1. **Define model** in `models.py`:
   ```python
   class NewModel(GlobalOpsBase):
       name = models.CharField(max_length=255)
   ```

2. **Create migration**:
   ```bash
   uv run python backend/manage.py makemigrations
   ```

3. **Apply migration**:
   ```bash
   uv run python backend/manage.py migrate
   ```

4. **Create Pydantic schemas** in `schemas.py`

5. **Create API endpoints** in `router.py`

6. **Register router** in `makerdb/api.py`

7. **Add admin configuration** in `admin.py` (optional)

## Adding a New Django App

```bash
# Create app
uv run python backend/manage.py startapp newapp

# Add to INSTALLED_APPS in settings.py
INSTALLED_APPS = [
    # ...
    "newapp",
]
```

## Debugging

```python
# Use Python debugger
import pdb; pdb.set_trace()

# Or breakpoint() (Python 3.7+)
breakpoint()

# Print SQL queries
from django.db import connection
print(connection.queries)
```

## Code Quality

```bash
# Lint code
uv run ruff check backend

# Format code
uv run ruff format backend

# Fix auto-fixable issues
uv run ruff check backend --fix
```

---

For more information:
- [Django Documentation](https://docs.djangoproject.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [pytest Documentation](https://docs.pytest.org/)
