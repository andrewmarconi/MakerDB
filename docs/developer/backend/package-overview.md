# Package Overview

## Django 6.0.1
Provides the foundation of the application:
- **ORM**: Object-relational mapping with support for complex queries
- **Migrations**: Schema versioning and management
- **Admin**: Auto-generated admin interface (enhanced with Jazzmin)
- **Authentication**: Built-in user authentication system
- **Middleware**: Request/response processing

**Documentation**: https://docs.djangoproject.com/

## FastAPI
High-performance async framework for building APIs:
- **Automatic OpenAPI/Swagger documentation**
- **Pydantic validation** - Type-safe request/response schemas
- **Async support** - Native async/await for I/O operations
- **Dependency injection** - Clean, testable code architecture
- **High performance** - Built on Starlette and Pydantic

**Documentation**: https://fastapi.tiangolo.com/

## Pydantic
Data validation using Python type annotations:
- Automatic request/response validation
- Clear error messages
- Editor support with autocomplete
- Serialization/deserialization

## pytest & pytest-django
Modern testing framework:
- Fixture-based test architecture
- Parallel test execution
- Database transaction handling
- Django-specific assertions and utilities

**Documentation**: https://docs.pytest.org/ & https://pytest-django.readthedocs.io/

## Ruff
Fast linter and formatter that replaces multiple tools:
- Linting (replaces flake8, pylint)
- Formatting (replaces black)
- Import sorting (replaces isort)
- ~10-100x faster than alternatives

**Documentation**: https://docs.astral.sh/ruff/
