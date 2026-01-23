# Smart Search Implementation Plan

Issue: #1 - Incorporate Smart Search

## Overview

Implement Typesense-powered search across the MakerDB application, starting with storage locations as a proof-of-concept.

## Architecture

```
Frontend (Nuxt, localhost:3000)
    │
    ├─→ /db/**  ──→ Nitro Proxy ──→ FastAPI (/api/db/**) ──→ Django ORM
    │
    └─→ /api/search/** ──→ Nitro Proxy ──→ FastAPI (/api/search) ──→ Typesense
```

**Key insight:** FastAPI already brokers Django data access via `/db/**`. Search uses `/api/search/**` through the same FastAPI layer for consistency.

### Request Flow
1. User types in global search box
2. Nuxt calls `/api/search/locations?q=shelf`
3. Nitro proxies to `http://localhost:8000/api/search/locations`
4. FastAPI `/search` router queries Typesense (with API key added server-side)
5. Results returned to frontend

---

## Phase 1: Infrastructure & Backend (COMPLETED)

### 1.1 Add Typesense to Docker Compose

```yaml
# docker-compose.yml
services:
  typesense:
    image: typesense/typesense:29.0
    restart: always
    ports:
      - "8108:8108"
    volumes:
      - typesense_data:/data
    environment:
      TYPESENSE_API_KEY: ${TYPESENSE_API_KEY}
      TYPESENSE_DATA_DIR: /data
      TYPESENSE_ENABLE_CORS: "true"
    command: --data-dir /data --api-key=${TYPESENSE_API_KEY}

volumes:
  typesense_data:
```

### 1.2 Environment Variables

Added to `.env`:
```
TYPESENSE_API_KEY=your-typesense-api-key
```

### 1.3 Python Dependencies

```bash
uv add typesense httpx
```

### 1.4 Custom Typesense Integration

Created `backend/core/typesense.py` with:
- `TypesenseRegistry` - singleton for managing collections and client
- `TypesenseCollection` - base class for defining collections
- `StorageCollection` - collection for Storage model
- Signal-based sync via `post_save` and `post_delete`

### 1.5 Django App Configuration

Updated `backend/inventory/apps.py` to register Storage collection on app ready.

### 1.6 FastAPI Search Router

Created `backend/search/router.py` with:
- `/search/locations` - Search storage locations
- `/search/locations/suggestions` - Autocomplete suggestions
- API key handled server-side (never exposed to browser)

### 1.7 Nitro Proxy Configuration

Updated `frontend/nuxt.config.ts`:
```typescript
nitro: {
  routeRules: {
    '/db/**': { proxy: 'http://localhost:8000/api/**' },
    '/api/search/**': { proxy: 'http://localhost:8000/api/search/**' }
  }
}
```

### 1.8 Initial Sync Command

Created `backend/inventory/management/commands/sync_typesense.py`:
```bash
uv run python backend/manage.py sync_typesense
```

---

## Phase 2: Frontend Implementation (COMPLETED)

### 2.1 Search Composable

Created `frontend/app/composables/useSmartSearch.ts`:
- `results` - readonly ref of search results
- `loading` - readonly ref for loading state
- `query` - readonly ref of current query
- `search(query, entity)` - perform search
- `clear()` - clear results

### 2.2 Global Search Component

Created `frontend/app/components/GlobalSearch.vue`:
- Input with search icon and Cmd+K shortcut hint
- Debounced search (150ms)
- Results dropdown with animations
- Loading state
- No results state
- Keyboard navigation (Escape to close)

### 2.3 Layout Integration

Updated `frontend/app/layouts/default.vue` to use `<GlobalSearch />` in the header.

---

## Files Created/Modified

### Backend
- `docker-compose.yml` - Added Typesense service
- `.env` - Added TYPESENSE_API_KEY
- `backend/core/typesense.py` - Custom Typesense integration (NEW)
- `backend/inventory/apps.py` - Register Storage collection (MODIFIED)
- `backend/inventory/management/commands/sync_typesense.py` - Initial sync (NEW)
- `backend/search/router.py` - FastAPI search endpoints (NEW)
- `backend/makerdb/api.py` - Added search router (MODIFIED)

### Frontend
- `frontend/nuxt.config.ts` - Added search proxy (MODIFIED)
- `frontend/app/composables/useSmartSearch.ts` - Search composable (NEW)
- `frontend/app/components/GlobalSearch.vue` - Search component (NEW)
- `frontend/app/layouts/default.vue` - Use GlobalSearch (MODIFIED)

---

## Summary of Key Decisions

| Decision | Choice |
|----------|--------|
| Sync strategy | Custom Django signals (avoid django-typesense compat issues) |
| Scope for v0.1 | Locations only |
| Frontend approach | Custom composable (simpler, full control) |
| Search behavior | Navigate to result page |
| Typesense hosting | Docker Compose |
| API access | FastAPI proxy (`/api/search/*`) with server-side API key |
| Autocomplete | Built-in (2+ chars trigger, 150ms debounce) |
| Filters (v0.1) | None (global search only) |

---

## Deployment Steps

1. **Start Docker services:**
   ```bash
   docker compose up -d
   ```

2. **Generate Typesense API key:**
   ```bash
   openssl rand -hex 32
   ```
   Add to `.env` as `TYPESENSE_API_KEY`

3. **Restart services** to pick up new config

4. **Run initial sync:**
   ```bash
   uv run python backend/manage.py sync_typesense
   ```

5. **Test search** at http://localhost:3000

---

## Future Enhancements (Post-v0.1)

1. **Parts search** - Add Part model to Typesense with fields:
   - Designator, Part Type, Footprint, Manufacturer, Project
2. **vue-instantsearch integration** - For faceted filtering UI
3. **Part selection** - For BOM manager component selection
4. **Advanced filters** - isEmpty/isNotEmpty for locations
5. **Search analytics** - Track popular queries, no-result searches
