<script setup lang="ts" generic="T">
import { useStorage } from '@vueuse/core'
import type { DropdownMenuItem } from '@nuxt/ui'
import type { tDataListViewProps } from '#shared/types'
import { type tModelKeys, MODEL_REGISTRY } from '#shared/config/models'
const props = withDefaults(defineProps<tDataListViewProps>(), {
  viewMode: 'table',
  canView: true,
  canDelete: true,
  canCreate: true,
  canSearch: true,
  canColumnToggle: true,
  canPaginate: true,
  itemsPerPage: 25,
  createLabel: undefined,
  emptyMessage: undefined,
})

const emit = defineEmits<{
  error: [error: Error]
  deleted: [id: string]
}>()

const slots = useSlots()
defineSlots<{
  [K: `${string}-cell`]: (props: { row: any, getValue: () => any }) => any;
  'card-body'?: (props: { item: T }) => any;
  'card-footer'?: (props: { item: T }) => any;
  'toolbar-actions'?: () => any;
  'empty'?: () => any;
}>()

const route = useRoute()
const storageKey = computed(() => `datalistview-${props.modelKey}-${route.path.replace(/\//g, '-')}`)
const search = ref('')
const viewMode = useStorage(`datalistview-${storageKey.value}-viewMode`, props.viewMode)
watch(() => props.viewMode, (val) => {
  viewMode.value = val
})
const columnVisibility = useStorage<Record<string, boolean>>(`datalistview-${storageKey.value}-columns`, {})
const page = ref(1)

// Filter state - initialize with filter keys from props
const filterValues = reactive<Record<string, any>>(
  props.filters?.reduce((acc, filter) => {
    acc[filter.key] = undefined
    return acc
  }, {} as Record<string, any>) || {}
)

const modelConfig = computed<typeof MODEL_REGISTRY[ModelKeys]>(() => {
  const config = MODEL_REGISTRY[props.modelKey as ModelKeys]
  if (!config) {
    console.warn(`Model key "${props.modelKey}" not found in MODEL_REGISTRY`)
  }
  return config
})

const baseApiPath = computed(() => modelConfig.value?.apiPath || '')

// Use search endpoint when searching, otherwise use regular endpoint
const apiPath = computed(() => {
  if (search.value && baseApiPath.value === '/db/inventory/locations') {
    return '/db/search/locations'
  }
  return baseApiPath.value
})

const detailRoute = computed(() => props.detailRoute || modelConfig.value?.detailRoute || '')
const createButtonLabel = computed(() => props.createLabel || `New ${modelConfig.value?.label || 'Item'}`)
const emptyStateMessage = computed(() => props.emptyMessage || `No ${modelConfig.value?.labelPlural || 'items'} found.`)

const createRoute = computed(() => `${detailRoute.value}/new`)
const getDetailRoute = (item: any) => `${detailRoute.value}/${item.id}`

const skip = computed(() => (page.value - 1) * props.itemsPerPage)

const itemsQuery = computed(() => {
  const params: Record<string, any> = { skip: skip.value, limit: props.itemsPerPage }

  // Use 'q' parameter for search endpoint, 'search' for regular endpoints
  if (search.value) {
    if (apiPath.value.includes('/search/')) {
      params.q = search.value
    } else {
      params.search = search.value
    }
  }

  if (props.defaultSort && !search.value) {
    // Sorting only applies to non-search queries (search has its own relevance ordering)
    const order = props.defaultSort.desc ? '-' : ''
    params.ordering = `${order}${props.defaultSort.id}`
  }

  // Add filter values to query params
  if (props.filters) {
    props.filters.forEach(filter => {
      const value = filterValues[filter.key]
      if (value !== undefined && value !== null && value !== '') {
        params[filter.key] = value
      }
    })
  }

  return params
})

// Fetch items and count in a single call for search, separate calls for regular listing
const { data: dataResponse, pending, error, refresh } = await useAsyncData(
  `${props.modelKey}-data`,
  async () => {
    const res = await $fetch<any>(apiPath.value, { params: itemsQuery.value })

    // Handle different response formats
    if (apiPath.value.includes('/search/')) {
      // Search endpoint returns { results: [], count: number }
      return {
        items: res.results || [],
        count: res.count || 0
      }
    } else {
      // Regular endpoint returns T[], need separate count call
      const countParams: Record<string, any> = {}

      // Add filter values to count query (but not skip/limit/ordering)
      if (props.filters) {
        props.filters.forEach(filter => {
          const value = filterValues[filter.key]
          if (value !== undefined && value !== null && value !== '') {
            countParams[filter.key] = value
          }
        })
      }

      const countRes = await $fetch<{ count: number }>(`${baseApiPath.value}/count`, { params: countParams })

      return {
        items: Array.isArray(res) ? res : [],
        count: countRes.count || 0
      }
    }
  },
  { watch: [itemsQuery] }
)

const items = computed(() => dataResponse.value?.items || [])
const total = computed(() => dataResponse.value?.count || 0)
const totalPages = computed(() => Math.ceil(total.value / props.itemsPerPage))

const visibleColumns = computed(() => {
  return props.columnDefs.filter(col => {
    const key = col.id as string || col.accessorKey as string
    return columnVisibility.value[key] !== false
  })
})

const getColumnSlotKey = (col: any) => {
  const key = col.id || col.accessorKey
  return `${key}-cell`
}

function getStatusColor(status: string) {
  if (!status) return 'neutral'
  const statusLower = status.toLowerCase()
  const colorMap: Record<string, "success" | "warning" | "info" | "error" | "neutral" | "primary"> = {
    active: 'success',
    draft: 'warning',
    completed: 'success',
    archived: 'neutral',
    open: 'info',
    ordered: 'warning',
    received: 'success',
    linked: 'info',
    local: 'warning',
    meta: 'primary',
    subassembly: 'success',
    'sub-assembly': 'success',
    in_stock: 'success',
    low_stock: 'warning',
    out_of_stock: 'error',
    both: 'primary'
  }
  return colorMap[statusLower] || 'neutral'
}

const columnToggleItems = computed<DropdownMenuItem[]>(() => {
  return props.columnDefs.map((col) => {
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

const showDeleteModal = ref(false)
const itemToDelete = ref<any>(null)
const isDeleting = ref(false)

function confirmDelete(item: any) {
  itemToDelete.value = item
  showDeleteModal.value = true
}

async function handleDelete() {
  if (!itemToDelete.value) return
  isDeleting.value = true
  try {
    await $fetch(`${apiPath.value}/${itemToDelete.value.id}`, {
      method: 'DELETE'
    })
    emit('deleted', itemToDelete.value.id)
    showDeleteModal.value = false
    await refresh()
  } catch (err) {
    emit('error', err as Error)
  } finally {
    isDeleting.value = false
  }
}

function handleRowClick(event: any) {
  const row = event?.row
  if (!row) return
  const item = row.original || row
  if (props.canView && item) {
    navigateTo(getDetailRoute(item))
  }
}

function getDetailRouteFromItem(item: T) {
  if (!props.canView) return null
  return getDetailRoute(item)
}
</script>

<template>
  <div class="space-y-6">
    <div v-if="modelConfig">
      <h1 class="text-2xl font-bold">{{ modelConfig.title }}</h1>
      <p class="text-gray-500 dark:text-gray-400">{{ modelConfig.description }}</p>
    </div>

    <UAlert
      v-if="error"
      color="error"
      title="There was a problem loading data"
      :description="error.message"
      icon="i-lucide-terminal"
    />

    <UCard v-if="canSearch || canColumnToggle || canCreate || filters">
      <div class="flex flex-col gap-4 mb-4">
        <div class="flex flex-col md:flex-row gap-4">
          <UInput
            v-if="canSearch"
            v-model="search"
            icon="i-heroicons-magnifying-glass"
            placeholder="Search..."
            class="flex-1"
            @keydown.enter="page = 1"
          />
          <div class="flex items-center gap-2 ml-auto">
            <slot name="toolbar-actions" />
            <UButton
              :color="viewMode === 'table' ? 'primary' : 'neutral'"
              :variant="viewMode === 'table' ? 'solid' : 'ghost'"
              icon="i-heroicons-table-cells"
              size="sm"
              @click="viewMode = 'table'"
            />
            <UButton
              :color="viewMode === 'grid' ? 'primary' : 'neutral'"
              :variant="viewMode === 'grid' ? 'solid' : 'ghost'"
              icon="i-heroicons-squares-2x2"
              size="sm"
              @click="viewMode = 'grid'"
            />
            <UDropdownMenu v-if="canColumnToggle" :items="columnToggleItems">
              <template #default>
                <UButton icon="i-heroicons-view-columns" color="neutral" variant="ghost" />
              </template>
            </UDropdownMenu>
            <UButton
              v-if="canCreate"
              icon="i-heroicons-plus"
              :label="createButtonLabel"
              color="primary"
              :to="createRoute"
            />
          </div>
        </div>

        <!-- Filters Row -->
        <div v-if="filters && filters.length > 0" class="flex flex-wrap gap-3">
          <template v-for="filter in filters" :key="filter.key">
            <USelect
              v-if="filter.type === 'select'"
              v-model="filterValues[filter.key]"
              :placeholder="filter.label"
              :items="filter.options"
              value-key="value"
              clearable
              class="w-48"
              @update:model-value="page = 1"
            />
            <UInput
              v-else-if="filter.type === 'input'"
              v-model="filterValues[filter.key]"
              :placeholder="filter.label"
              class="w-48"
              @keydown.enter="page = 1"
            />
          </template>
          <UButton
            v-if="Object.values(filterValues).some(v => v !== undefined && v !== null && v !== '')"
            icon="i-heroicons-x-mark"
            label="Clear filters"
            color="neutral"
            variant="ghost"
            size="sm"
            @click="() => { Object.keys(filterValues).forEach(k => filterValues[k] = undefined); page = 1 }"
          />
        </div>
      </div>
    </UCard>

    <USkeleton v-if="pending" class="h-96" />
    <div v-else-if="!pending && (!items || items.length === 0)" class="text-center py-12 text-gray-500">
      <slot name="empty">
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
      </slot>
    </div>

    <template v-else>
      <UTable
        v-if="viewMode === 'table'"
        :data="items"
        :columns="visibleColumns"
        class="w-full"
        @row-click="handleRowClick"
      >
        <template v-for="col in visibleColumns" :key="col.id || col.accessorKey" #[getColumnSlotKey(col)]="slotProps">
          <template v-if="slots[getColumnSlotKey(col)]">
            <component :is="() => slots[getColumnSlotKey(col)]!(slotProps)" />
          </template>
          <template v-else>
            <NuxtLink
              v-if="canView && getColumnSlotKey(col).replace('-cell', '') === modelConfig?.clickableColumn && getDetailRoute(slotProps.row.original)"
              :to="getDetailRoute(slotProps.row.original)!"
              class="font-medium text-primary-500 hover:underline"
            >
              {{ slotProps.getValue() }}
            </NuxtLink>
            <span v-else>{{ slotProps.getValue() }}</span>
          </template>
        </template>
        <template v-if="canDelete" #body-row="{ row }">
          <UDropdownMenu
            v-if="tableActions && tableActions.length > 0"
            :items="tableActions.map(action => ({
              label: action.label,
              icon: action.icon,
              onClick: () => action.onClick(row.original || row)
            }))"
          >
            <UButton icon="i-heroicons-ellipsis-horizontal" variant="ghost" color="neutral" />
          </UDropdownMenu>
        </template>
      </UTable>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        <UCard v-for="item in items" :key="(item as any).id">
          <template #header>
            <NuxtLink
              v-if="canView && modelConfig?.clickableColumn && getDetailRouteFromItem(item)"
              :to="getDetailRouteFromItem(item)!"
              class="font-medium text-primary-500 hover:underline"
            >
              {{ (item as any)[modelConfig!.clickableColumn] }}
            </NuxtLink>
            <span v-else-if="modelConfig?.clickableColumn" class="font-medium">{{ (item as any)[modelConfig!.clickableColumn] }}</span>
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

          <template v-if="cardActions && cardActions.length > 0" #footer>
            <UDropdownMenu
              :items="cardActions.map(action => ({
                label: action.label,
                icon: action.icon,
                onClick: () => action.onClick(item)
              }))"
            >
              <UButton icon="i-heroicons-ellipsis-horizontal" variant="ghost" color="neutral" />
            </UDropdownMenu>
          </template>
          <template v-else-if="canDelete" #footer>
            <UButton
              icon="i-heroicons-trash"
              label="Delete"
              color="error"
              variant="ghost"
              @click="confirmDelete(item)"
            />
          </template>
        </UCard>
      </div>
    </template>

    <div v-if="canPaginate && totalPages > 1" class="flex justify-center mt-4">
      <UPagination
        v-model:page="page"
        :total="total"
        :items-per-page="itemsPerPage"
        :show-controls="true"
      />
    </div>

    <UModal v-model:open="showDeleteModal">
      <template #body>
        <UCard>
          <template #header>
            <h3 class="text-lg font-semibold">Delete {{ modelConfig?.label }}</h3>
          </template>
          <p class="text-gray-500">Are you sure you want to delete this {{ modelConfig?.label?.toLowerCase() }}? This action cannot be undone.</p>
          <template #footer>
            <div class="flex justify-end gap-2">
              <UButton label="Cancel" color="neutral" @click="showDeleteModal = false" />
              <UButton
                label="Delete"
                color="error"
                :loading="isDeleting"
                @click="handleDelete"
              />
            </div>
          </template>
        </UCard>
      </template>
    </UModal>
  </div>
</template>
