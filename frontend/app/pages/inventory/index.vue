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

async function fetchParts() {
  const skip = (page.value - 1) * ITEMS_PER_PAGE
  let url = `/db/parts/?skip=${skip}&limit=${ITEMS_PER_PAGE}`

  const [data, countData] = await Promise.all([
    $fetch<Part[]>(url),
    $fetch<{ count: number }>('/db/parts/count')
  ])
  total.value = countData?.count || 0
  return data
}
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
      :can-search="false"
      :server-side-pagination="true"
      :total="total"
      :items-per-page="ITEMS_PER_PAGE"
      :default-sort="{ id: 'name', desc: false }"
      :fetch-fn="fetchParts"
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
  </div>
</template>
