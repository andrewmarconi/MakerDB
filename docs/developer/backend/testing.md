# Testing

## Running Tests

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest backend/tests/test_models.py

# Run with verbose output
uv run pytest -v

# Run with coverage
uv run pytest --cov=backend

# Recreate test database
uv run pytest --create-db
```

## Test Configuration

Tests are configured in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "makerdb.settings"
python_files = ["test_*.py", "*_test.py"]
pythonpath = "backend"
addopts = "--reuse-db"  # Faster tests by reusing database
```

## Writing Tests

### Model Tests

```python
# backend/tests/test_models.py
import pytest
from parts.models import Part
from core.models import Company

@pytest.mark.django_db
class TestPartModel:
    def test_create_part(self):
        part = Part.objects.create(
            name="Resistor 10k",
            description="1/4W through-hole"
        )
        assert part.id is not None
        assert part.name == "Resistor 10k"

    def test_part_with_manufacturer(self):
        mfr = Company.objects.create(
            name="Yageo",
            is_manufacturer=True
        )
        part = Part.objects.create(
            name="RC0805",
            manufacturer=mfr
        )
        assert part.manufacturer.name == "Yageo"
```

### API Tests

```python
# backend/tests/test_api.py
import pytest
from httpx import AsyncClient
from asgiref.sync import async_to_sync

@pytest.mark.django_db
@pytest.mark.asyncio
async def test_list_parts():
    from makerdb.asgi import application

    async with AsyncClient(app=application, base_url="http://test") as client:
        response = await client.get("/api/parts/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

@pytest.mark.django_db
@pytest.mark.asyncio
async def test_create_part():
    from makerdb.asgi import application

    async with AsyncClient(app=application, base_url="http://test") as client:
        data = {"name": "Test Part", "description": "Test"}
        response = await client.post("/api/parts/", json=data)
        assert response.status_code == 201
        assert response.json()["name"] == "Test Part"
```

## Fixtures

Create reusable test data in `tests/conftest.py`:

```python
import pytest
from core.models import Company
from parts.models import Part

@pytest.fixture
def manufacturer():
    return Company.objects.create(
        name="Test Manufacturer",
        is_manufacturer=True
    )

@pytest.fixture
def sample_part(manufacturer):
    return Part.objects.create(
        name="Sample Part",
        manufacturer=manufacturer
    )
```
