# MakerDB Phased Implementation Plan

This plan outlines the development of the MakerDB frontend using Nuxt 4, Nuxt UI, and TailwindCSS. The implementation is divided into 8 phases to ensure a logical build-up of features.

## Proposed Changes

### Phase 1: Foundation & Navigation Refinements
Focus on setting up the core scaffolding and ensuring a premium look and feel.

#### [MODIFY] [default.vue](file:///Users/andrew/Develop/MakerDB/frontend/app/layouts/default.vue)
- Refine sidebar with sub-navigation for Inventory and Projects.
- Add breadcrumbs and page title handling.
- Improve dark mode transitions.

#### [NEW] [components](file:///Users/andrew/Develop/MakerDB/frontend/app/components/)
- `AppHeader.vue`: Reusable header with search and user menu.
- `AppSidebar.vue`: Extracted sidebar component.
- `StatusBadge.vue`: Generic status indicator for parts, orders, etc.

---

### Phase 2: Parts & Inventory Core
Implement the primary data views for parts and stock levels.

#### [NEW] [pages/inventory/index.vue](file:///Users/andrew/Develop/MakerDB/frontend/app/pages/inventory/index.vue)
- Data table for parts with fuzzy search.
- Filters for part types (Linked, Local, Meta).

#### [NEW] [pages/inventory/[id].vue](file:///Users/andrew/Develop/MakerDB/frontend/app/pages/inventory/[id].vue)
- Detailed view of a part.
- Tabs for: Specifications, Stock, History, Attachments.

---

### Phase 3: Storage & Locations
Manage the physical organization of the inventory.

#### [NEW] [pages/locations/index.vue](file:///Users/andrew/Develop/MakerDB/frontend/app/pages/locations/index.vue)
- Tree view for hierarchical storage locations.
- QR code display for locations.

---

### Phase 4: Projects & BOMs
Handle the Bill of Materials workflow.

#### [NEW] [pages/projects/index.vue](file:///Users/andrew/Develop/MakerDB/frontend/app/pages/projects/index.vue)
- List of projects with status and valuation.

#### [NEW] [pages/projects/[id]/bom.vue](file:///Users/andrew/Develop/MakerDB/frontend/app/pages/projects/[id]/bom.vue)
- Interactive BOM table.
- CSV/TSV import modal with column mapping.
- Automatic matching and substitute selection UI.

---

### Phase 5: Purchasing & Orders
Procurement management.

#### [NEW] [pages/purchasing/index.vue](file:///Users/andrew/Develop/MakerDB/frontend/app/pages/purchasing/index.vue)
- Purchase order list (Open, Ordered, Received).

#### [NEW] [pages/purchasing/[id].vue](file:///Users/andrew/Develop/MakerDB/frontend/app/pages/purchasing/[id].vue)
- Order detail view.
- "Receive Items" wizard for lot control.

---

### Phase 6: Search & Scanning
Advanced discovery and physical interaction.

#### [NEW] [components/Search/ParametricSearch.vue](file:///Users/andrew/Develop/MakerDB/frontend/app/components/Search/ParametricSearch.vue)
- Unit-aware filter (e.g., matching 10k to 10000).

#### [NEW] [composables/useScanner.ts](file:///Users/andrew/Develop/MakerDB/frontend/app/composables/useScanner.ts)
- Composable for handling camera or HID barcode scanners.

---

### Phase 7: Custom Fields & Attachments
Extensibility and documentation.

#### [NEW] [components/Files/AttachmentManager.vue](file:///Users/andrew/Develop/MakerDB/frontend/app/components/Files/AttachmentManager.vue)
- Drag-and-drop file upload.
- Gallery view for images and PDFs.

---

### Phase 8: Reporting & Polish
Final dashboard and data visualization.

#### [MODIFY] [index.vue](file:///Users/andrew/Develop/MakerDB/frontend/app/pages/index.vue)
- Add charts for inventory valuation over time.
- Low stock summary cards.

## Verification Plan

### Automated Tests
- `npm run test:unit`: Verify utility functions (e.g., unit conversions).
- `npm run test:nuxt`: Verify component rendering and basic navigation.

---

### Phase 9: Backend API Integration
Connect the mock frontend to the existing Django/FastAPI backend.

#### [NEW] [backend/schemas](file:///Users/andrew/Develop/MakerDB/backend/)
- Create Pydantic schemas for `Part`, `Storage`, `Stock`, `Project`, and `Order`.
- Ensure schema fields align with both Django models and frontend expectations.

#### [NEW] [backend/routers](file:///Users/andrew/Develop/MakerDB/backend/)
- Implement FastAPI routers for each app:
  - `parts_router.py`
  - `inventory_router.py`
  - `projects_router.py`
  - `procurement_router.py`
- Mount routers in [api.py](file:///Users/andrew/Develop/MakerDB/backend/makerdb/api.py).

#### [MODIFY] [frontend/app/composables](file:///Users/andrew/Develop/MakerDB/frontend/app/composables/)
- Create `useApiFetch.ts` using Nuxt's `useFetch` with custom defaults (base URL, headers).
- Replace mock data in pages with real API calls.

## Verification Plan

### Automated Tests
- `npm run test:unit`: Verify utility functions.
- `pytest`: Run backend API tests (using `httpx` and `pytest-django`).

### Manual Verification
1.  **Data Persistence**: Create a part in the UI and verify it appears in the Django Admin (`/cp/`).
2.  **Real-time Updates**: Verify that stock adjustments in the frontend are reflected in the database.
