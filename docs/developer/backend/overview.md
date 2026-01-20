# Overview

The MakerDB backend uses a hybrid architecture combining **Django 6.0.1** for ORM, admin, and migrations with **FastAPI** for high-performance REST API endpoints. Both frameworks run in a single ASGI process, sharing authentication and database access.

## Key Features
- Hybrid Django + FastAPI architecture
- Type-safe API with Pydantic validation
- Async-capable FastAPI endpoints
- Django admin panel with Jazzmin theme
- PostgreSQL 17 database
- Comprehensive test coverage with pytest
