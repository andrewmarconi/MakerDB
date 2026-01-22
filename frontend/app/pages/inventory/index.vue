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
      :default-sort="{ id: 'name', desc: false }"
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
