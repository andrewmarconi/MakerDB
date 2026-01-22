<script setup lang="ts">
import type { ColumnDef } from '@tanstack/vue-table'

definePageMeta({
  title: 'Inventory'
})

useSeoMeta({
  title: 'Inventory',
  description: 'Manage your parts and track stock levels.'
})

const columns: ColumnDef<Part>[] = [
  { accessorKey: 'name', header: 'Name' },
  { accessorKey: 'mpn', header: 'MPN' },
  { accessorKey: 'part_type', header: 'Type', enableSorting: false },
  { accessorKey: 'total_stock', header: 'Stock' }
]

const cardFields = ['part_type', 'total_stock', 'mpn']

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

    if (sorting.value.length > 0) {
      const sort = sorting.value[0]!
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

watch([page, sorting], () => {
  fetchParts()
}, { deep: true })

onMounted(fetchParts)
</script>

<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-2xl font-bold">Inventory</h1>
      <p class="text-gray-500 dark:text-gray-400">Manage your parts and track stock levels.</p>
    </div>

    <DataListView
      model-key="inventory"
      :column-defs="columns"
      :card-fields="cardFields"
      :can-paginate="false"
      :can-search="false"
      :default-sort="{ id: 'name', desc: false }"
      :loading="pending"
      :data="parts"
    >
      <template #part_type-cell="{ row }">
        <UBadge
          :color="row.original.part_type === 'local' ? 'warning' : row.original.part_type === 'linked' ? 'info' : row.original.part_type === 'meta' ? 'primary' : 'success'"
          variant="subtle"
          size="sm"
        >
          {{ row.original.part_type }}
        </UBadge>
      </template>

      <template #total_stock-cell="{ row }">
        <div class="font-mono">{{ row.original.total_stock ?? 0 }}</div>
      </template>
    </DataListView>

    <div v-if="total > ITEMS_PER_PAGE" class="flex justify-center mt-4">
      <UPagination
        v-model:page="page"
        :total="total"
        :items-per-page="ITEMS_PER_PAGE"
        :show-controls="true"
      />
    </div>
  </div>
</template>
