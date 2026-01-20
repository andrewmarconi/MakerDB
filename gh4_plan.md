# Implementation Plan: Common Data Table/Grid Component (Issue #4)

## Branch Name
`feat/common-data-table-grid-component`

## Overview
Create a reusable `DataTable.vue` component that standardizes data views across the application, supporting both table and grid layouts with common features like sorting, filtering, pagination, and column visibility.

## Issue Requirements
1. ✅ View Type: Grid, Table
2. ✅ Default Sorting
3. ✅ Filtering Options
4. ✅ Column Visibility Options
5. ✅ Pagination
6. ✅ Make designated column clickable in tables (e.g., Name)
7. ✅ Include ability for user to switch between list and grid-with-cards view

## Architecture Overview

**Three Component System:**
1. `DataTable.vue` - Main component
2. `DataTableFilter.vue` - External filter UI (optional)
3. `DataTableActions.vue` - Configurable actions component (for cards/rows)

## Component: `frontend/app/components/DataTable.vue`

### Props Interface (TypeScript)
```typescript
interface DataTableProps<T> {
  // Data & Columns
  data: T[]
  columns: ColumnDef<T>[]

  // View Mode
  viewMode?: 'table' | 'grid'  // Default: 'table'
  storageKey?: string  // Default: current route path

  // Card View Configuration
  cardFields: string[]  // Fields to display in card view
  cardActions?: ActionConfig[]  // Actions for card footer

  // Table Actions
  tableActions?: ActionConfig[]  // Actions for table rows

  // Sorting
  defaultSort?: { id: string; desc: boolean }

  // Filtering
  searchable?: boolean  // Default: false (searches all columns)
  filterUI?: DataTableFilter  // External filter component

  // Column Visibility
  showColumnToggle?: boolean  // Default: true

  // Pagination
  paginatable?: boolean  // Default: true
  itemsPerPage?: number  // Default: 25

  // Clickable Column/Row
  clickableColumn?: string  // Column key that's clickable
  onRowClick?: (row: T) => void | RouteLocationRaw

  // Display Options
  emptyState?: string | Component
  loading?: boolean
}

interface ActionConfig {
  label: string
  icon: string
  onClick: (row: any) => void
  variant?: 'default' | 'destructive'
}
```

### Slots (following UTable pattern)
```vue
<DataTable :data="items" :columns="columns">
  <!-- Custom header slots -->
  <template #[columnKey]-header="{ column }">
    Custom header content
  </template>

  <!-- Custom cell slots -->
  <template #[columnKey]-cell="{ row, column, getValue }">
    Custom cell content
  </template>

  <!-- Card customization slots -->
  <template #card-header="{ item }">
    Custom card header
  </template>

  <template #card-body="{ item }">
    Custom card body
  </template>

  <template #card-footer="{ item }">
    Custom card actions
  </template>
</DataTable>
```

### Component Structure
```
DataTable.vue
├── Filter UI (if filterUI prop provided)
├── Controls Bar (top, inside UCard)
│   ├── Search Input (if searchable=true) - searches all columns
│   ├── View Toggle (ButtonGroup: Table | Grid)
│   └── Column Visibility Dropdown (UDropdownMenu with checkboxes)
├── Table View (when viewMode='table')
│   └── UTable with sorting, pagination, column-visibility
│       └── Expose slots for custom cell rendering
├── Grid View (when viewMode='grid')
│   └── Responsive grid (1→2→3→4 columns) of UCards
│       ├── Default card layout (uses cardFields + cardActions)
│       └── Expose slots for customization (card-header, card-body, card-footer)
└── Pagination (bottom, when paginatable=true)
    └── UPagination
```

## Key Implementation Details

### 1. LocalStorage Persistence
```typescript
// Generate storage key from route path
const route = useRoute()
const storageKey = computed(() => props.storageKey || route.path.replace(/\//g, '-'))

// View mode persistence
const viewMode = useStorage(`datatable-${storageKey.value}-viewMode`, 'table')

// Column visibility persistence
const columnVisibility = useStorage(`datatable-${storageKey.value}-columns`, {})
```

### 2. Search Implementation (searches all columns)
```typescript
const search = ref('')
const filteredData = computed(() => {
  if (!search.value) return data.value
  return data.value.filter(item =>
    columns.value.some(col => {
      const val = item[col.accessorKey]
      return val && String(val).toLowerCase().includes(search.value.toLowerCase())
    })
  )
})
```

### 3. Custom Cell Rendering via Slots
```vue
<UTable :columns="visibleColumns" :data="filteredData">
  <template v-for="col in visibleColumns" :key="col.accessorKey" #[col.accessorKey]="{ row, column, getValue }">
    <slot :name="`${col.accessorKey}-cell`" :row="row" :column="column" :getValue="getValue">
      {{ getValue() }}
    </slot>
  </template>
</UTable>
```

### 4. Card Actions (configurable per page)
```vue
<template #card-footer="{ item }">
  <UDropdownMenu
    v-if="cardActions?.length"
    :items="cardActions.map(action => ({
      label: action.label,
      icon: action.icon,
      onClick: () => action.onClick(item)
    }))"
  >
    <UButton icon="i-heroicons-ellipsis-horizontal" variant="ghost" />
  </UDropdownMenu>
  <slot v-else name="card-footer" :item="item" />
</template>
```

### 5. External Filter UI Integration
```vue
<component
  v-if="filterUI"
  :is="filterUI"
  v-model="externalFilters"
  @filter-change="handleExternalFilterChange"
/>
```

## Component: `frontend/app/components/DataTableFilter.vue` (Optional Helper)

### Purpose
Provide a standardized filter UI that can be passed to DataTable via `filterUI` prop.

### Props
```typescript
interface DataTableFilterProps {
  filters: FilterConfig[]
  modelValue: Record<string, any>
}

interface FilterConfig {
  key: string
  label: string
  type: 'select' | 'input' | 'date'
  options?: { label: string; value: any }[]
}
```

## Implementation Tasks

### Phase 1: Create DataTable Component
1. Create `frontend/app/components/DataTable.vue` with `<script setup lang="ts">`
2. Define props interface with all options
3. Define slots: `#<column>-header`, `#<column>-cell`, `#card-header`, `#card-body`, `#card-footer`
4. Implement view mode state with localStorage persistence (route-based key)
5. Implement column visibility state with localStorage persistence
6. Build table view using `UTable` with v-model bindings
7. Build grid view using responsive grid with `UCard`
8. Implement search input (searches all columns)
9. Add view mode toggle (segmented buttons)
10. Add column visibility dropdown
11. Add pagination with `UPagination`
12. Implement clickable column logic (NuxtLink wrapper)
13. Add loading state (skeleton)
14. Add empty state component
15. Expose custom cell slots
16. Emit `row-click` event when onRowClick is provided
17. Integrate external filter UI if provided

### Phase 2: Create DataTableFilter Component
1. Create `frontend/app/components/DataTableFilter.vue`
2. Define props for filter configuration
3. Implement select filters with `USelect`
4. Implement input filters with `UInput`
5. Emit filter changes to parent
6. Add tests for filter component

### Phase 3: Create Tests
1. Create `frontend/test/unit/DataTable.spec.ts`
2. Test props validation
3. Test view mode switching and localStorage persistence
4. Test column visibility toggle and persistence
5. Test search (all columns)
6. Test pagination
7. Test clickable column navigation
8. Test custom cell slots
9. Test card actions configuration
10. Test external filter UI integration
11. Nuxt integration test in `frontend/test/nuxt/DataTable.test.ts`

### Phase 4: Migrate Existing Pages

#### Projects Page (`frontend/app/pages/projects/index.vue`)
- Replace current UTable implementation with DataTable
- Define `cardFields`: `['status', 'revision', 'updated_at']`
- Define `tableActions`: View, Edit
- Enable searchable
- Set clickableColumn to 'name'
- Remove all pagination/filter logic (handled by component)
- Add `#status-cell` slot for badge rendering

#### Inventory Page (`frontend/app/pages/inventory/index.vue`)
- Migrate complex custom table to DataTable
- Define `cardFields`: `['mpn', 'part_type', 'total_stock']`
- Define `tableActions`: View Stock, Print Label
- Keep existing filter type dropdown as external filter UI
- Set clickableColumn to 'name'
- Add custom slots for part_type badge, stock display
- Note: Replace current `UInput` + `USelect` with `DataTableFilter` component

#### Purchasing Page (`frontend/app/pages/purchasing/index.vue`)
- Replace simple UTable with DataTable
- Define `cardFields`: `['vendor', 'status', 'total', 'date']`
- Define `tableActions`: View Order
- Enable searchable
- Set clickableColumn to 'vendor' or add NuxtLink in cell
- Add `#status-cell` slot for StatusBadge

#### BOMTable Component (`frontend/app/components/BOMTable.vue`)
- Replace with DataTable using custom slots
- Define `cardFields`: `['quantity', 'mpn', 'status']`
- Define custom `tableActions` for BOM-specific actions
- Add custom slots:
  - `#designators-cell`: Font-mono designators list
  - `#match-cell`: Part link or "Match Part" button
  - `#status-cell`: Matched/Unmatched badge
  - `#actions-cell`: Custom actions dropdown
- Note: Keep component name, but use DataTable internally

### Phase 5: Documentation
1. Create `frontend/components/DataTable.md` with:
   - Props interface documentation
   - Slots documentation
   - Usage examples (table view, grid view, with filters, with custom slots)
   - Migration guide from existing implementations
2. Update AGENTS.md with DataTable usage patterns

## Usage Examples

### Basic Table View
```vue
<script setup lang="ts">
const columns = [
  { accessorKey: 'name', header: 'Project Name' },
  { accessorKey: 'status', header: 'Status' },
  { accessorKey: 'updated_at', header: 'Last Modified' }
]

const { data: projects } = await useAsyncData('projects', () =>
  $fetch<Project[]>('/db/projects/')
)
</script>

<template>
  <DataTable
    :data="projects"
    :columns="columns"
    clickable-column="name"
    default-sort="{ id: 'updated_at', desc: true }"
  />
</template>
```

### With Grid View & Card Fields
```vue
<template>
  <DataTable
    :data="items"
    :columns="columns"
    :card-fields="['type', 'status', 'date']"
    :card-actions="[{ label: 'Edit', icon: 'i-heroicons-pencil', onClick: editItem }]"
    clickable-column="name"
  />
</template>
```

### With Custom Cell Slots (BOMTable-style)
```vue
<template>
  <DataTable :data="items" :columns="columns">
    <template #designators-cell="{ row }">
      <span class="font-mono text-xs">{{ row.designators.join(', ') }}</span>
    </template>

    <template #status-cell="{ row }">
      <UBadge :color="row.status === 'matched' ? 'green' : 'red'">
        {{ row.status }}
      </UBadge>
    </template>
  </DataTable>
</template>
```

### With External Filter UI
```vue
<script setup>
const filters = [
  { key: 'type', label: 'Type', type: 'select', options: partTypes }
]

const externalFilters = ref({ type: 'All' })
</script>

<template>
  <DataTable
    :data="items"
    :columns="columns"
    :filter-ui="DataTableFilter"
    :filters="filters"
    v-model:external-filters="externalFilters"
  />
</template>
```

## Technical Decisions Summary

1. **Card Fields**: Use separate `cardFields` array prop (✅ confirmed)
2. **Search**: Searches all columns by default (✅ confirmed)
3. **Persistence**: Yes, store view mode and column visibility to localStorage (✅ confirmed)
4. **Grid Layout**: Default responsive breakpoints (1/2/3/4 columns) (✅ confirmed)
5. **BOMTable**: Migrate to use DataTable internally with custom slots (✅ confirmed)
6. **External Filters**: Define separate `DataTableFilter` component and data structure (✅ confirmed)
7. **Custom Cell Renderers**: Yes, expose slots matching UTable pattern (✅ confirmed)
8. **Card Actions**: Yes, configurable via `cardActions` prop per page (✅ confirmed)
9. **LocalStorage Key**: Auto-generated from route path, with optional override prop (✅ confirmed)
