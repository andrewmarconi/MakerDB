# DataListView Refactor Plan

> Issue: #45 - Common UI for listview pages
> Status: Planning
> Created: 2026-01-22

## Overview

Refactor `DataTable.vue` into `DataListView.vue` - a self-contained, convention-based component that handles data fetching, CRUD operations, and display modes internally.

## Goals

1. **Simplify page components** - Pages should only define what's unique (columns, card fields)
2. **Centralize data fetching** - Component manages its own data lifecycle via `useAsyncData`
3. **Convention over configuration** - Use `modelKey` to derive API paths, routes, and labels
4. **Consistent UX** - Built-in loading, error, empty states, and delete confirmation

## Current State

Each listview page currently:
- Fetches its own data with `useAsyncData` or `useApiFetch`
- Manages loading/error states
- Defines redundant props (`createRoute`, `createLabel`, `onRowClick`, etc.)
- Implements its own delete confirmation modal

**Example (projects/index.vue) - 58 lines:**
```vue
<script setup>
const { data, pending, error } = await useAsyncData(...)
const isLoading = computed(() => pending.value || !!error.value)
</script>

<template>
  <div class="space-y-6">
    <div>
      <h1>Projects</h1>
      <p>Description...</p>
    </div>
    <template v-if="error">
      <UAlert ... />
    </template>
    <DataTable
      :data="data"
      :columns="columns"
      :card-fields="cardFields"
      searchable
      clickable-column="name"
      :loading="isLoading"
      :on-row-click="(item) => ({ path: `/projects/${item.id}` })"
      create-route="/projects/new"
      create-label="New Project"
    />
  </div>
</template>
```

## Proposed State

**Example (projects/index.vue) - ~20 lines:**
```vue
<script setup>
const columns = [
  { accessorKey: 'name', header: 'Project Name' },
  { accessorKey: 'status', header: 'Status' },
  { accessorKey: 'revision', header: 'Revision' }
]
const cardFields = ['status', 'revision', 'updated_at']
</script>

<template>
  <DataListView
    model-key="projects"
    :column-defs="columns"
    :card-fields="cardFields"
  />
</template>
```

## Model Registry

Create `shared/config/models.ts`:

```ts
export type ModelConfig = {
  /** API endpoint path (e.g., '/db/projects') */
  apiPath: string;
  /** Singular label (e.g., 'Project') */
  label: string;
  /** Plural label (e.g., 'Projects') */
  labelPlural: string;
  /** Frontend route for detail pages (e.g., '/projects') */
  detailRoute: string;
  /** Page title */
  title: string;
  /** Page description */
  description: string;
  /** Default clickable column */
  clickableColumn?: string;
};

export const MODEL_REGISTRY: Record<string, ModelConfig> = {
  projects: {
    apiPath: '/db/projects',
    label: 'Project',
    labelPlural: 'Projects',
    detailRoute: '/projects',
    title: 'Projects',
    description: 'Manage your Bill of Materials and calculate production costs.',
    clickableColumn: 'name',
  },
  inventory: {
    apiPath: '/db/parts',
    label: 'Part',
    labelPlural: 'Parts',
    detailRoute: '/inventory',
    title: 'Inventory',
    description: 'Manage your parts and track stock levels.',
    clickableColumn: 'name',
  },
  locations: {
    apiPath: '/db/inventory/locations',
    label: 'Location',
    labelPlural: 'Locations',
    detailRoute: '/locations',
    title: 'Storage Locations',
    description: 'Browse and manage your storage locations.',
    clickableColumn: 'name',
  },
  companies: {
    apiPath: '/db/companies',
    label: 'Company',
    labelPlural: 'Companies',
    detailRoute: '/companies',
    title: 'Companies',
    description: 'Manage manufacturers and vendors.',
    clickableColumn: 'name',
  },
  purchasing: {
    apiPath: '/db/procurement/orders',
    label: 'Order',
    labelPlural: 'Orders',
    detailRoute: '/purchasing',
    title: 'Purchasing',
    description: 'Track your component orders and manage supplier relationships.',
    clickableColumn: 'order_id',
  },
} as const;

export type ModelKey = keyof typeof MODEL_REGISTRY;
```

## New Props Interface

```ts
export type DataListViewProps = {
  /** Model key from MODEL_REGISTRY - determines API, routes, labels */
  modelKey: ModelKey;

  /** Column definitions (TanStack Table ColumnDef format) */
  columnDefs: ColumnDef<any>[];

  /** Fields to display in grid/card view */
  cardFields?: string[];

  /** Display mode - 'table' for rows, 'grid' for cards (default: 'table') */
  viewMode?: 'table' | 'grid';

  // Capability flags (all default to true)
  /** Show clickable link to detail page */
  canView?: boolean;
  /** Show delete action on rows */
  canDelete?: boolean;
  /** Show "New" button in toolbar */
  canCreate?: boolean;
  /** Show search input */
  canSearch?: boolean;
  /** Show column visibility toggle */
  canColumnToggle?: boolean;
  /** Enable pagination */
  canPaginate?: boolean;

  /** Default sort configuration */
  defaultSort?: { id: string; desc: boolean };

  /** Custom filter UI component */
  filterUI?: Component;

  /** Number of items per page (default: 25) */
  itemsPerPage?: number;

  /** Override create button label (default: "New {label}") */
  createLabel?: string;

  /** Override empty state message (default: "No {labelPlural} found.") */
  emptyMessage?: string;
};
```

## Component Internal Structure

```vue
<script setup lang="ts">
import { MODEL_REGISTRY, type ModelKey } from '#shared/config/models'

const props = withDefaults(defineProps<DataListViewProps>(), {
  viewMode: 'table',
  canView: true,
  canDelete: true,
  canCreate: true,
  canSearch: true,
  canColumnToggle: true,
  canPaginate: true,
  itemsPerPage: 25,
})

const emit = defineEmits<{
  error: [error: Error]
  deleted: [id: string]
}>()

// Get model config
const config = computed(() => MODEL_REGISTRY[props.modelKey])

// Data fetching with useAsyncData
const { data, pending, error, refresh } = await useAsyncData(
  `${props.modelKey}-list`,
  () => $fetch(config.value.apiPath),
  { watch: [() => props.modelKey] }
)

// Computed labels
const createButtonLabel = computed(() =>
  props.createLabel || `New ${config.value.label}`
)
const emptyStateMessage = computed(() =>
  props.emptyMessage || `No ${config.value.labelPlural} found.`
)

// Routes
const createRoute = computed(() => `${config.value.detailRoute}/new`)
const getDetailRoute = (item: any) => `${config.value.detailRoute}/${item.id}`

// Delete handling
const showDeleteModal = ref(false)
const itemToDelete = ref<any>(null)
const isDeleting = ref(false)

async function handleDelete() {
  if (!itemToDelete.value) return
  isDeleting.value = true
  try {
    await $fetch(`${config.value.apiPath}/${itemToDelete.value.id}`, {
      method: 'DELETE'
    })
    emit('deleted', itemToDelete.value.id)
    showDeleteModal.value = false
    refresh()
  } catch (err) {
    emit('error', err as Error)
  } finally {
    isDeleting.value = false
  }
}
</script>
```

## Template Structure

```vue
<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div>
      <h1 class="text-2xl font-bold">{{ config.title }}</h1>
      <p class="text-gray-500 dark:text-gray-400">{{ config.description }}</p>
    </div>

    <!-- Error State -->
    <UAlert
      v-if="error"
      color="error"
      title="There was a problem loading data"
      :description="error.message"
      icon="i-lucide-terminal"
    />

    <!-- Toolbar -->
    <UCard v-if="canSearch || canColumnToggle || canCreate">
      <div class="flex flex-col md:flex-row gap-4">
        <UInput v-if="canSearch" v-model="search" ... />
        <div class="flex items-center gap-2 ml-auto">
          <!-- View toggle buttons -->
          <!-- Column toggle dropdown -->
          <UButton
            v-if="canCreate"
            icon="i-heroicons-plus"
            :label="createButtonLabel"
            color="primary"
            :to="createRoute"
          />
        </div>
      </div>
    </UCard>

    <!-- Loading State -->
    <USkeleton v-if="pending" class="h-96" />

    <!-- Empty State -->
    <div v-else-if="!data?.length" class="text-center py-12 text-gray-500">
      <UIcon name="i-heroicons-folder-open" class="w-12 h-12 mx-auto mb-4 opacity-50" />
      <p>{{ emptyStateMessage }}</p>
      <UButton
        v-if="canCreate"
        icon="i-heroicons-plus"
        :label="createButtonLabel"
        color="primary"
        :to="createRoute"
        class="mt-4"
      />
    </div>

    <!-- Data Display -->
    <template v-else>
      <UTable v-if="viewMode === 'table'" ... />
      <div v-else class="grid ...">
        <!-- Card grid -->
      </div>
    </template>

    <!-- Pagination -->
    <UPagination v-if="canPaginate && totalPages > 1" ... />

    <!-- Delete Confirmation Modal -->
    <UModal v-model:open="showDeleteModal">
      ...
    </UModal>
  </div>
</template>
```

## Slots for Customization

```vue
defineSlots<{
  // Custom cell renderers
  [K: `${string}-cell`]: (props: { row: any, getValue: () => any }) => any;

  // Custom card content
  'card-body'?: (props: { item: T }) => any;

  // Toolbar additions (before create button)
  'toolbar-actions'?: () => any;

  // Custom empty state
  'empty'?: () => any;
}>()
```

## Migration Plan

### Phase 1: Create New Component
1. Create `shared/config/models.ts` with MODEL_REGISTRY
2. Create `components/DataListView.vue` with new implementation
3. Update `shared/types/ui.ts` with new types

### Phase 2: Migrate Pages (one at a time)
1. `projects/index.vue` - simplest case
2. `purchasing/index.vue` - test custom cell slots
3. `companies/index.vue` - test delete functionality
4. `locations/index.vue` - test with card actions
5. `inventory/index.vue` - test server-side pagination (may need `fetchFn` override)

### Phase 3: Cleanup
1. Remove old `DataTable.vue` once all pages migrated
2. Remove old `DataTableProps` type
3. Update any documentation

## Edge Cases to Handle

1. **Server-side pagination** (inventory) - Add optional `fetchFn` prop override
2. **Custom cell renderers** - Keep slot system
3. **Additional toolbar buttons** (e.g., Import) - Add `toolbar-actions` slot
4. **Non-standard routes** - Add `detailRoute` override prop
5. **Conditional delete** (e.g., can't delete if has children) - Emit event, let page handle

## Files to Create/Modify

| File | Action |
|------|--------|
| `shared/config/models.ts` | Create |
| `shared/types/ui.ts` | Add `DataListViewProps`, keep old types during migration |
| `components/DataListView.vue` | Create |
| `pages/projects/index.vue` | Migrate |
| `pages/purchasing/index.vue` | Migrate |
| `pages/companies/index.vue` | Migrate |
| `pages/locations/index.vue` | Migrate |
| `pages/inventory/index.vue` | Migrate (needs fetchFn for pagination) |
| `components/DataTable.vue` | Delete after migration |

## Success Criteria

- [ ] All listview pages use `DataListView`
- [ ] Page components reduced to <30 lines each
- [ ] Delete confirmation works consistently
- [ ] Loading/error/empty states are consistent
- [ ] No regression in functionality
- [ ] Custom cell slots still work
- [ ] Server-side pagination still works for inventory
