# API Documentation

## Base URL

- **Development**: `http://localhost:8000/api`
- **Frontend Proxy**: `/db/**` proxied to `/api/**`

## Router Overview

All routers are registered in `backend/makerdb/api.py`:

| Router | Prefix | Tags | Description |
|--------|--------|------|-------------|
| `core_router` | `/core` | Core | Companies, attachments |
| `parts_router` | `/parts` | Parts | Components, designators |
| `inventory_router` | `/inventory` | Inventory | Stock, locations, lots |
| `projects_router` | `/projects` | Projects | Projects, BOMs |
| `procurement_router` | `/procurement` | Procurement | Orders, offers |

## Response Format

### Success Response
```json
{
  "id": "uuid",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z",
  "tags": [],
  "custom_fields": {}
}
```

### Error Response
```json
{
  "detail": "Error message"
}
```

## Core Endpoints (`/core`)

### Companies
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/core/companies` | List companies |
| GET | `/core/companies/count` | Count companies |
| GET | `/core/companies/{id}` | Get company |
| POST | `/core/companies` | Create company |
| PUT | `/core/companies/{id}` | Update company |
| DELETE | `/core/companies/{id}` | Delete company |

### Attachments
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/core/attachments` | List attachments |
| GET | `/core/attachments/{id}` | Get attachment |
| POST | `/core/attachments` | Upload attachment |
| PUT | `/core/attachments/{id}` | Update attachment |
| DELETE | `/core/attachments/{id}` | Delete attachment |

## Parts Endpoints (`/parts`)

### Parts
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/parts` | List parts with pagination |
| GET | `/parts/count` | Count parts |
| GET | `/parts/{id}` | Get part |
| POST | `/parts` | Create part |
| PUT | `/parts/{id}` | Update part |
| DELETE | `/parts/{id}` | Delete part |

### Designators
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/parts/designators` | List designators |
| POST | `/parts/designators` | Create designator |
| PUT | `/parts/designators/{id}` | Update designator |
| DELETE | `/parts/designators/{id}` | Delete designator |

## Inventory Endpoints (`/inventory`)

### Locations
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/inventory/locations` | List storage locations |
| GET | `/inventory/locations/count` | Count locations |
| GET | `/inventory/locations/{id}` | Get location |
| POST | `/inventory/locations` | Create location |
| PUT | `/inventory/locations/{id}` | Update location |
| DELETE | `/inventory/locations/{id}` | Delete location |

### Stock
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/inventory/stock` | List stock entries |
| GET | `/inventory/stock/{id}` | Get stock entry |
| POST | `/inventory/stock` | Create stock entry |
| PUT | `/inventory/stock/{id}` | Update stock |
| DELETE | `/inventory/stock/{id}` | Delete stock |

### Lots
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/inventory/lots` | List lots |
| GET | `/inventory/lots/{id}` | Get lot |
| POST | `/inventory/lots` | Create lot |
| PUT | `/inventory/lots/{id}` | Update lot |
| DELETE | `/inventory/lots/{id}` | Delete lot |

## Projects Endpoints (`/projects`)

### Projects
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/projects` | List projects |
| GET | `/projects/count` | Count projects |
| GET | `/projects/{id}` | Get project |
| POST | `/projects` | Create project |
| PUT | `/projects/{id}` | Update project |
| DELETE | `/projects/{id}` | Delete project |

### BOM
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/projects/{id}/bom` | Get project BOM |
| POST | `/projects/{id}/bom` | Add BOM item |
| PUT | `/projects/{id}/bom` | Update BOM items |
| POST | `/projects/{id}/bom/import` | Import BOM from CSV |
| POST | `/projects/{id}/bom/match` | Match BOM to inventory |

## Procurement Endpoints (`/procurement`)

### Orders
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/procurement/orders` | List orders |
| GET | `/procurement/orders/count` | Count orders |
| GET | `/procurement/orders/{id}` | Get order |
| POST | `/procurement/orders` | Create order |
| PUT | `/procurement/orders/{id}` | Update order |
| DELETE | `/procurement/orders/{id}` | Delete order |

### Offers
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/procurement/offers` | List offers |
| GET | `/procurement/offers/{id}` | Get offer |
| POST | `/procurement/offers` | Create offer |
| PUT | `/procurement/offers/{id}` | Update offer |
| DELETE | `/procurement/offers/{id}` | Delete offer |

## Common Patterns

### Pagination
List endpoints return paginated results:
```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "page_size": 20
}
```

### Async Handling
All endpoints use `sync_to_async` for Django ORM operations. Responses are awaited properly in async routes.

### Schema Validation
- Creation requests use `XxxCreate` schemas
- Update requests use `XxxUpdate` schemas (with `extra="forbid"`)
- Response schemas inherit from `GlobalOpsSchema` (includes `id`, `tags`, `custom_fields`)

## Frontend API Usage

Use the `useApiFetch` composable for all API calls:

```typescript
const { data, error } = await useApiFetch('/parts')

// POST request
await apiPost('/parts', partData)

// PUT request
await apiPut(`/parts/${id}`, updateData)

// DELETE request
await apiDelete(`/parts/${id}`)
```

## Testing Endpoints

### Backend Tests
```bash
uv run pytest                           # All tests
uv run pytest backend/tests/            # Test directory
uv run pytest backend/tests/test_*.py   # Specific file
```

### Test Database
- Tests use `--reuse-db` by default for speed
- Use `--create-db` to recreate the test database fresh
- All tests require `@pytest.mark.django_db` marker
