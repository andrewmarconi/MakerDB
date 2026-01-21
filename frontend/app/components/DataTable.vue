<script setup lang="ts" generic="T">
import { useStorage } from '@vueuse/core'
import type { ColumnDef } from '@nuxt/ui'
import type { DropdownMenuItem } from '@nuxt/ui'

interface ActionConfig {
  label: string
  icon: string
  onClick: (row: any) => void
  variant?: 'default' | 'destructive'
}

interface Props<T> {
  data: T[]
  columns: ColumnDef<T>[]
  viewMode?: 'table' | 'grid'
  storageKey?: string
  cardFields: string[]
  cardActions?: ActionConfig[]
  tableActions?: ActionConfig[]
  defaultSort?: { id: string; desc: boolean }
  searchable?: boolean
  filterUI?: any
  showColumnToggle?: boolean
  paginatable?: boolean
  itemsPerPage?: number
  clickableColumn?: string
  onRowClick?: (row: T) => void | { path: string }
  emptyState?: string | any
  loading?: boolean
}

interface Props<T> {
  data: T[]
  columns: ColumnDef<T>[]
  viewMode?: 'table' | 'grid'
  storageKey?: string
  cardFields: string[]
  cardActions?: ActionConfig[]
  tableActions?: ActionConfig[]
  defaultSort?: { id: string; desc: boolean }
  searchable?: boolean
  filterUI?: any
  showColumnToggle?: boolean
  paginatable?: boolean
  itemsPerPage?: number
  clickableColumn?: string
  onRowClick?: (row: T) => void | { path: string }
  emptyState?: string | any
  loading?: boolean
}

const props = withDefaults(defineProps<Props<T>>(), {
  viewMode: 'table',
  showColumnToggle: true,
  paginatable: true,
  itemsPerPage: 25,
  searchable: false
})

const emit = defineEmits<{
  'row-click': [row: T]
}>()

const route = useRoute()
const storageKey = computed(() => props.storageKey || route.path.replace(/\//g, '-'))

const search = ref('')

const viewMode = useStorage(`datatable-${storageKey.value}-viewMode`, props.viewMode)

const columnVisibility = useStorage(`datatable-${storageKey.value}-columns`, {})

const page = ref(1)

const visibleColumns = computed(() => {
  return props.columns.filter(col => {
    const key = col.id as string || col.accessorKey as string
    return columnVisibility.value[key] !== false
  })
})

const getColumnSlotKey = (col: any) => {
  const key = col.id || col.accessorKey
  return `${key}-cell`
}

const sortedData = computed(() => {
  const data = filteredData.value
  if (!data || data.length === 0) return []

  const sortKey = props.defaultSort?.id
  if (!sortKey) return data

  return [...data].sort((a: any, b: any) => {
    const aVal = a[sortKey]
    const bVal = b[sortKey]
    const desc = props.defaultSort?.desc ?? false

    if (aVal === bVal) return 0
    if (aVal < bVal) return desc ? 1 : -1
    return desc ? -1 : 1
  })
})

const filteredData = computed(() => {
  if (!props.data) return []

  if (!search.value) return props.data

  return props.data.filter((item: any) =>
    props.columns.some((col: any) => {
      const key = col.id || col.accessorKey
      const val = item[key]
      return val && String(val).toLowerCase().includes(search.value.toLowerCase())
    })
  )
})

const totalPages = computed(() => Math.ceil(filteredData.value.length / props.itemsPerPage))

const paginatedData = computed(() => {
  if (!props.paginatable) return sortedData.value

  const start = (page.value - 1) * props.itemsPerPage
  const end = start + props.itemsPerPage
  return sortedData.value.slice(start, end)
})

function handleRowClick(event: any) {
  const row = event?.row
  if (!row) return
  const item = row.original || row
  if (props.onRowClick && item) {
    const result = props.onRowClick(item)
    if (result && typeof result === 'object' && 'path' in result) {
      navigateTo(result.path)
    }
  }
  emit('row-click', item)
}

function getDetailRoute(row: any) {
  if (!row) return null
  if (!props.clickableColumn || !props.onRowClick) return null
  const item = row.original || row
  if (!item) return null
  const result = props.onRowClick(item)
  if (result && typeof result === 'object' && 'path' in result) {
    return result.path
  }
  return null
}

function getDetailRouteFromItem(item: T) {
  if (!props.clickableColumn || !props.onRowClick) return null
  const result = props.onRowClick(item)
  if (result && typeof result === 'object' && 'path' in result) {
    return result.path
  }
  return null
}

function getStatusColor(status: string) {
  if (!status) return 'gray'
  const statusLower = status.toLowerCase()
  const colorMap: Record<string, string> = {
    active: 'green',
    draft: 'amber',
    completed: 'green',
    archived: 'gray',
    open: 'blue',
    ordered: 'yellow',
    received: 'green',
    linked: 'blue',
    local: 'orange',
    meta: 'purple',
    subassembly: 'green',
    'sub-assembly': 'green',
    in_stock: 'green',
    low_stock: 'orange',
    out_of_stock: 'red',
    both: 'purple'
  }
  return colorMap[statusLower] || 'gray'
}

const columnToggleItems = computed<DropdownMenuItem[]>(() => {
  return props.columns.map((col) => {
    const key = (col.id || col.accessorKey) as string
    return {
      label: (col.header as string) || key,
      type: 'checkbox' as const,
      checked: columnVisibility.value[key] !== false,
      onUpdateChecked: (checked: boolean) => {
        columnVisibility.value[key] = checked
      }
    }
  })
})
</script>

<template>
  <div class="space-y-4">
    <UCard v-if="searchable || showColumnToggle">
      <div class="flex flex-col md:flex-row gap-4 mb-4">
        <UInput
          v-if="searchable"
          v-model="search"
          icon="i-heroicons-magnifying-glass"
          placeholder="Search..."
          class="flex-1"
        />
        <div class="flex items-center gap-2">
          <UButton
            :color="viewMode === 'table' ? 'primary' : 'gray'"
            :variant="viewMode === 'table' ? 'solid' : 'ghost'"
            icon="i-heroicons-table-cells"
            size="sm"
            @click="viewMode = 'table'"
          />
          <UButton
            :color="viewMode === 'grid' ? 'primary' : 'gray'"
            :variant="viewMode === 'grid' ? 'solid' : 'ghost'"
            icon="i-heroicons-squares-2x2"
            size="sm"
            @click="viewMode = 'grid'"
          />
          <UDropdownMenu v-if="showColumnToggle" :items="columnToggleItems">
            <template #default>
              <UButton icon="i-heroicons-view-columns" color="gray" variant="ghost" />
            </template>
          </UDropdownMenu>
        </div>
      </div>
    </UCard>

    <USkeleton v-if="loading" class="h-96" />

    <div v-else-if="paginatedData.length === 0" class="text-center py-12 text-gray-500">
      <UIcon name="i-heroicons-folder-open" class="w-12 h-12 mx-auto mb-4 opacity-50" />
      <p>No items found.</p>
    </div>

    <template v-else>
      <UTable
        v-if="viewMode === 'table'"
        :data="paginatedData"
        :columns="visibleColumns"
        class="w-full"
        @row-click="handleRowClick"
      >
        <template v-for="col in visibleColumns" :key="col.id || col.accessorKey" #[getColumnSlotKey(col)]="{ row, column, getValue }">
          <slot
            :name="getColumnSlotKey(col)"
            :row="row"
            :column="column"
            :getValue="getValue"
          >
            <NuxtLink
              v-if="getColumnSlotKey(col).replace('-cell', '') === clickableColumn && getDetailRoute(row)"
              :to="getDetailRoute(row)"
              class="font-medium text-primary-500 hover:underline"
            >
              {{ getValue() }}
            </NuxtLink>
            <span v-else>{{ getValue() }}</span>
          </slot>
        </template>
      </UTable>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        <UCard v-for="item in paginatedData" :key="(item as any).id">
          <template #header>
            <NuxtLink
              v-if="clickableColumn && getDetailRouteFromItem(item)"
              :to="getDetailRouteFromItem(item)"
              class="font-medium text-primary-500 hover:underline"
            >
              {{ (item as any)[clickableColumn] }}
            </NuxtLink>
            <span v-else class="font-medium">{{ (item as any)[clickableColumn] }}</span>
          </template>

          <div class="space-y-2">
            <slot name="card-body" :item="item">
              <div v-for="field in cardFields" :key="field" class="flex justify-between items-center">
                <span class="text-sm text-gray-500 capitalize">{{ field.replace(/_/g, ' ') }}</span>
                <UBadge
                  v-if="field === 'status'"
                  :color="getStatusColor((item as any)[field])"
                  variant="subtle"
                  size="xs"
                >
                  {{ (item as any)[field] }}
                </UBadge>
                <span v-else class="text-sm">{{ (item as any)[field] }}</span>
              </div>
            </slot>
          </div>

          <template #footer>
            <UDropdownMenu
              v-if="cardActions && cardActions.length > 0"
              :items="cardActions.map(action => ({
                label: action.label,
                icon: action.icon,
                onClick: () => action.onClick(item)
              }))"
            >
              <UButton icon="i-heroicons-ellipsis-horizontal" variant="ghost" color="gray" />
            </UDropdownMenu>
            <slot v-else name="card-footer" :item="item" />
          </template>
        </UCard>
      </div>
    </template>

    <div v-if="paginatable && totalPages > 1" class="flex justify-center mt-4">
      <UPagination
        v-model:page="page"
        :total="filteredData.length"
        :items-per-page="itemsPerPage"
        :show-controls="true"
      />
    </div>
  </div>
</template>
