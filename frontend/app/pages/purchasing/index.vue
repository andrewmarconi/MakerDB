<script setup lang="ts">
import type { ColumnDef } from '@tanstack/vue-table'

definePageMeta({
  title: 'Purchasing'
})

interface Order {
  id: string
  order_id: string
  vendor: { name: string }
  status: string
  total: number
  date: string
}

const columns: ColumnDef<Order>[] = [
  { accessorKey: 'order_id', header: 'Order ID' },
  { accessorKey: 'vendor', header: 'Vendor' },
  { accessorKey: 'status', header: 'Status' },
  { accessorKey: 'total', header: 'Total' },
  { accessorKey: 'date', header: 'Order Date' }
]

const cardFields = ['vendor', 'status', 'total', 'date']

const { data, pending, error } = await useAsyncData(
  'orders',
  (_nuxtApp, { signal }) => $fetch<Order[]>('/db/orders/', { signal }),
)

const isLoading = computed(() => {
  if (pending) return true;
  if (error) return true;
  return false;
})
</script>

<template>
  <div class="space-y-6">
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold">Purchasing</h1>
        <p class="text-gray-500 dark:text-gray-400">Track your component orders and manage supplier relationships.</p>
      </div>
      <div class="flex items-center gap-2">
        <UButton icon="i-heroicons-plus" label="New Order" color="primary" />
      </div>
    </div>

    <template v-if="error">
      <UAlert 
        color="error"
        title="There was a problem loading data"
        :description="error.message"
        icon="i-lucide-terminal"
       />
    </template>
    <DataTable 
      :data="data as Order[]" 
      :columns="columns" 
      :card-fields="cardFields" 
      searchable
      clickable-column="order_id" 
      :loading="!isLoading"
      :on-row-click="(item) => ({ path: `/purchasing/${item.id}` })">
      <template #status-cell="{ row }">
        <StatusBadge :status="row.original.status" />
      </template>
    </DataTable>
  </div>
</template>
