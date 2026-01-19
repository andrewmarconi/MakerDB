<script setup>
const columns = [
  { id: 'order_id', key: 'id', label: 'Order ID', sortable: true },
  { id: 'vendor', key: 'vendor', label: 'Vendor', sortable: true },
  { id: 'status', key: 'status', label: 'Status' },
  { id: 'total', key: 'total', label: 'Total', sortable: true },
  { id: 'date', key: 'date', label: 'Order Date', sortable: true },
  { id: 'actions', key: 'actions', label: '' }
]

const { data: orders, refresh } = await useApiFetch('/procurement/orders/')
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

    <UCard>
      <UTable :columns="columns" :rows="orders">
        <template #status-data="{ row }">
          <StatusBadge :status="row.status" />
        </template>

        <template #actions-data="{ row }">
          <div class="flex justify-end">
            <UButton variant="ghost" color="gray" icon="i-heroicons-eye" :to="`/purchasing/${row.id}`" />
          </div>
        </template>
      </UTable>
    </UCard>
  </div>
</template>
