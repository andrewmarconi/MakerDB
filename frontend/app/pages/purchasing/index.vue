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

const { data: orders, refresh } = await useApiFetch('/procurement/orders/')

const orderData = computed(() => orders.value ?? [])
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

    <DataTable
      v-if="orders"
      :data="orderData"
      :columns="columns"
      :card-fields="cardFields"
      searchable
      clickable-column="order_id"
      :on-row-click="(order) => ({ path: `/purchasing/${order.id}` })"
    >
      <template #status-cell="{ row }">
        <StatusBadge :status="row.status" />
      </template>
    </DataTable>

    <UCard v-else>
      <div class="flex items-center justify-center py-12">
        <UIcon name="i-heroicons-arrow-path" class="w-8 h-8 animate-spin text-primary-500" />
        <span class="ml-3">Loading orders...</span>
      </div>
    </UCard>
  </div>
</template>
