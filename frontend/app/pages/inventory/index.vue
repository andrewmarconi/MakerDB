<script setup lang="ts">
import type { ColumnDef } from '@nuxt/ui'

definePageMeta({
  title: 'Inventory'
})

interface Part {
  id: string
  name: string
  mpn: string
  part_type: string
  total_stock: number
  manufacturer?: { name: string }
}

const columns: ColumnDef<Part>[] = [
  { accessorKey: 'name', header: 'Name' },
  { accessorKey: 'mpn', header: 'MPN' },
  { accessorKey: 'part_type', header: 'Type', enableSorting: false },
  { accessorKey: 'total_stock', header: 'Stock' }
]

const cardFields = ['part_type', 'total_stock']

const partTypes = [
  { label: 'All', value: 'All' },
  { label: 'Linked', value: 'Linked' },
  { label: 'Local', value: 'Local' },
  { label: 'Meta', value: 'Meta' },
  { label: 'Sub-assembly', value: 'Sub-assembly' }
]

const filterConfig = [
  { key: 'part_type', label: 'Type', type: 'select', options: partTypes }
]

const filters = ref<Record<string, any>>({ part_type: 'All' })
const ITEMS_PER_PAGE = 25
const page = ref(1)
const total = ref(0)
const parts = ref<Part[]>([])
const pending = ref(false)
const sorting = ref<{ id: string; desc: boolean }[]>([])

async function fetchParts() {
  pending.value = true
  try {
    const skip = (page.value - 1) * ITEMS_PER_PAGE
    let url = `/db/parts/?skip=${skip}&limit=${ITEMS_PER_PAGE}`

    const filters = filters.value
    if (filters.part_type && filters.part_type !== 'All') {
      url += `&part_type=${filters.part_type}`
    }

    if (sorting.value.length > 0) {
      const sort = sorting.value[0]
      const order = sort.desc ? '-' : ''
      url += `&ordering=${order}${sort.id}`
    }

    const [data, countData] = await Promise.all([
      $fetch<Part[]>(url),
      $fetch<{ count: number }>('/db/parts/count')
    ])
    parts.value = Array.isArray(data) ? data : []
    total.value = countData?.count || 0
  } catch (e) {
    console.error('Failed to fetch parts:', e)
    parts.value = []
    total.value = 0
  } finally {
    pending.value = false
  }
}

watch([page, filters, sorting], () => {
  page.value = 1
  fetchParts()
}, { deep: true })

const filteredItems = computed(() => {
  if (!parts.value) return []
  return (parts.value as Part[]).filter((item: Part) => {
    const matchesType = filters.value.part_type === 'All' || item.part_type === filters.value.part_type?.toLowerCase()
    return matchesType
  })
})

onMounted(fetchParts)
</script>

<template>
  <div class="space-y-6">
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold">Inventory</h1>
        <p class="text-gray-500 dark:text-gray-400">Manage your parts and track stock levels.</p>
      </div>
      <div class="flex items-center gap-2">
        <UButton icon="i-heroicons-plus" label="Add Part" color="primary" to="/inventory/new" />
        <UButton icon="i-heroicons-arrow-up-tray" label="Import" variant="ghost" color="gray" />
      </div>
    </div>

    <UCard>
      <DataTableFilter
        :filters="filterConfig"
        v-model="filters"
        @filter-change="() => { page.value = 1 }"
      />

      <div v-if="pending" class="flex justify-center py-12">
        <UIcon name="i-heroicons-arrow-path" class="w-8 h-8 animate-spin text-gray-400" />
      </div>

      <div v-else-if="!parts || parts.length === 0" class="text-center py-12 text-gray-500">
        <UIcon name="i-heroicons-circle-stack" class="w-12 h-12 mx-auto mb-4 opacity-50" />
        <p>No parts found.</p>
      </div>

      <DataTable
        v-else
        :data="filteredItems"
        :columns="columns"
        :card-fields="cardFields"
        clickable-column="name"
        :on-row-click="(part) => ({ path: `/inventory/${part.id}` })"
        :paginatable="false"
      >
        <template #part_type-cell="{ row }">
          <UBadge
            :color="row.part_type === 'local' ? 'gray' : row.part_type === 'linked' ? 'blue' : row.part_type === 'meta' ? 'purple' : 'green'"
            variant="subtle"
            size="sm"
          >
            {{ row.part_type }}
          </UBadge>
        </template>

        <template #total_stock-cell="{ row }">
          <div class="font-mono">{{ row.total_stock }}</div>
        </template>
      </DataTable>

      <div v-if="total > ITEMS_PER_PAGE" class="flex justify-center mt-4">
        <UPagination
          v-model:page="page"
          :total="total"
          :items-per-page="ITEMS_PER_PAGE"
          :show-controls="true"
        />
      </div>
    </UCard>
  </div>
</template>
