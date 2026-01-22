<script setup lang="ts">
import type { ColumnDef } from '@tanstack/vue-table'

definePageMeta({
  title: 'Purchasing'
})

useSeoMeta({
  title: 'Purchasing',
  description: 'Track your component orders and manage supplier relationships.'
})

const columns: ColumnDef<Order>[] = [
  { accessorKey: 'order_id', header: 'Order ID' },
  { accessorKey: 'vendor', header: 'Vendor' },
  { accessorKey: 'status', header: 'Status' },
  { accessorKey: 'total', header: 'Total' },
  { accessorKey: 'date', header: 'Order Date' }
]

const cardFields = ['vendor', 'status', 'total', 'date']
</script>

<template>
  <DataListView
    model-key="purchasing"
    :column-defs="columns"
    :card-fields="cardFields"
  >
    <template #status-cell="{ row }">
      <StatusBadge :status="row.original.status" />
    </template>
  </DataListView>
</template>
