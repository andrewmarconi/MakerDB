# Architecture Documentation

## Project Overview

**MakerDB** is a full-stack application for managing electronic components, projects, bills of materials (BOM), inventory, and procurement. It combines Django's ORM with FastAPI for async API endpoints, and uses Nuxt 4 for the frontend.

## Technology Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **Django 6.0** | ORM, Admin interface (Jazzmin), Sessions |
| **FastAPI 0.128+** | Async REST API endpoints |
| **PostgreSQL 17** | Primary database |
| **psycopg[binary]** | PostgreSQL adapter |
| **uvicorn** | ASGI server |
| **Pydantic** | Schema validation |

### Frontend
| Technology | Purpose |
|------------|---------|
| **Nuxt 4** | Vue 3 meta-framework with file-based routing |
| **Vue 3.5** | Composition API with `<script setup>` |
| **@nuxt/ui** | UI component library (Tailwind-based) |
| **@nuxt/eslint** | ESLint integration |
| **@vueuse/core** | Vue composables |
| **Vitest** | Testing framework |

### DevOps
- **Docker Compose**: PostgreSQL 17 container
- **uv**: Python package manager
- **npm**: Node.js package manager
- **Ruff**: Python linting

## Directory Structure

```
/Users/andrew/Develop/MakerDB/
├── backend/
│   ├── makerdb/              # Main Django project
│   │   ├── settings.py       # Django settings
│   │   ├── urls.py           # Root URL config (admin at /cp/)
│   │   ├── asgi.py           # ASGI config (mounts FastAPI at /api)
│   │   └── api.py            # FastAPI app with all routers
│   ├── core/                 # Shared entities (Companies, Attachments)
│   ├── parts/                # Parts management
│   ├── inventory/            # Stock, Storage, Lots
│   ├── projects/             # Projects, BOMs
│   ├── procurement/          # Orders, Offers
│   └── tests/                # pytest tests
├── frontend/
│   ├── app/
│   │   ├── components/       # Vue components
│   │   ├── composables/      # useApiFetch, etc.
│   │   ├── layouts/          # default.vue (sidebar layout)
│   │   ├── pages/            # File-based routing
│   │   ├── utils/            # Utilities
│   │   ├── app.vue           # Root component
│   │   └── app.config.ts     # App config
│   ├── test/                 # Vitest tests
│   └── nuxt.config.ts        # Nuxt configuration
├── docker-compose.yml        # PostgreSQL 17
├── pyproject.toml            # Python dependencies
└── README.md
```

## Backend Architecture

### Django Apps

#### core (Shared Entities)
| Model | Description |
|-------|-------------|
| `TimeStampedModel` | Abstract: created_at, updated_at |
| `GlobalOpsBase` | Abstract: UUID PK, tags, custom_fields |
| `Company` | Manufacturers/Vendors (is_manufacturer, is_vendor) |
| `Attachment` | File attachments (images, datasheets, invoices) |

#### parts (Component Management)
| Model | Description |
|-------|-------------|
| `Designator` | Electrical prefixes (R, C, U, etc.) |
| `Part` | Core component model with MPN, footprint, manufacturer FK |

#### inventory (Stock Management)
| Model | Description |
|-------|-------------|
| `Storage` | Physical locations (shelf, bin) |
| `Lot` | Batches of parts with optional Order FK |
| `Stock` | Part + Storage + Lot join with quantity |

#### projects (BOM Management)
| Model | Description |
|-------|-------------|
| `Project` | Project with status, revision |
| `BOMItem` | Project + Part join with quantity, designators |

#### procurement (Purchasing)
| Model | Description |
|-------|-------------|
| `Order` | Purchase orders with vendor FK, status |
| `Offer` | Vendor price offers for parts |

### Async Pattern

FastAPI routes use `sync_to_async` from `asgiref.sync` to wrap Django ORM calls:

```python
@router.get("/items")
async def list_items():
    @sync_to_async
    def _list():
        return list(Item.objects.all())
    return await _list()
```

## Frontend Architecture

### Nuxt 4 Structure

#### Pages (File-Based Routing)
```
app/pages/
├── index.vue              # Dashboard
├── companies/             # Company management
├── projects/              # Projects + BOM
├── inventory/             # Stock + Parts
├── locations/             # Storage locations
└── purchasing/            # Orders
```

#### Key Components
- `DataTable.vue` - Reusable table with search, pagination
- `BOMTable.vue` - BOM display with matching status
- `StatusBadge.vue` - Status color mapping

#### Composables
`useApiFetch.ts` - Centralized API client:
```typescript
useApiFetch<T>(url, options)  // Wrapper around useFetch
apiPost<T>(url, data)         // POST helper
apiPut<T>(url, data)          // PUT helper
apiDelete<T>(url)             // DELETE helper
```

### Frontend Patterns
- **Data Fetching**: `useAsyncData` for SSR-friendly fetching
- **State**: `useStorage` from @vueuse/core for persistent local state
- **Styling**: Tailwind CSS via @nuxt/ui

## Data Model Relationships

```
Company
├── Parts (manufacturer FK)
├── Orders (vendor FK)
└── Offers (vendor FK)

Part
├── Stock Entries (1:N)
├── Offers (1:N)
└── BOM Usage (1:N)

Stock
├── Part (FK)
├── Storage (FK)
└── Lot (FK, optional)

Lot
├── Order (FK, optional)
└── Stock Entries (1:N)

Order
├── Vendor (FK)
└── Lots (1:N)

Project
├── BOM Items (1:N)
└── Attachments (M:N)
```

## Configuration

### Environment Variables (.env)
- `SECRET_KEY` - Django secret key
- `DEBUG` - Debug mode
- `DATABASE_URL` - PostgreSQL connection string

### Nuxt Config
- **Modules**: @nuxt/ui, @nuxt/eslint
- **Nitro Proxy**: `/db/**` proxied to `http://localhost:8000/api/**`

## Testing

### Backend
```bash
uv run pytest                    # All tests
uv run pytest test_domain_phase2.py  # Single file
uv run pytest --create-db        # Fresh database
```

### Frontend
```bash
npm test           # All tests
npm run test:unit  # Unit tests only
npm run test:nuxt  # Nuxt integration tests
```

## Key Conventions

1. **Imports**: Standard library first, then third-party, then local. Absolute imports from project root.
2. **Type Hints**: Modern syntax (`list[str]`, not `List[str]`).
3. **Naming**: `snake_case` for functions/variables, `PascalCase` for classes.
4. **Line Length**: 120 characters (handled by ruff).
5. **Pydantic Schemas**: Separate read (`CompanySchema`) and write (`CompanyCreate`) schemas.
6. **Vue Components**: `<script setup>` with Composition API.
