<script setup>
definePageMeta({
  title: 'Order Details'
})

useSeoMeta({
  title: 'Order Details',
  description: 'View and manage purchase order details.'
})

const route = useRoute()
const id = route.params.id

// Mock order data
const { data: order, refresh } = await useApiFetch(`/procurement/orders/${route.params.id}`)

const columns = [
  { id: 'mpn', key: 'mpn', label: 'MPN' },
  { id: 'description', key: 'description', label: 'Description' },
  { id: 'quantity', key: 'quantity', label: 'Qty' },
  { id: 'price', key: 'price', label: 'Unit Price' },
  { id: 'subtotal', key: 'subtotal', label: 'Subtotal' }
]
const handleReceive = (items) => {
  console.log('Items received:', items)
  order.value.status = 'Received'
}
</script>

<template>
  <div class="space-y-6" v-if="order">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-4">
        <UButton variant="ghost" color="neutral" icon="i-heroicons-arrow-left" to="/purchasing" />
        <div>
          <h1 class="text-2xl font-bold flex items-center gap-2">
            {{ order.id }}
            <StatusBadge :status="order.status" />
          </h1>
          <p class="text-gray-500 dark:text-gray-400">Vendor: {{ order.vendor }} • Date: {{ order.date }}</p>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <ReceiveItemsModal :order="order" @receive="handleReceive" v-if="order.status === 'Ordered'" />
        <UButton label="Place Order" icon="i-heroicons-shopping-cart" color="primary" v-if="order.status === 'Open'" />
        <UDropdownMenu
          :items="[[{ label: 'Print Invoice', icon: 'i-heroicons-printer' }, { label: 'Cancel Order', icon: 'i-heroicons-x-circle' }]]">
          <UButton variant="ghost" color="neutral" icon="i-heroicons-ellipsis-horizontal" />
        </UDropdownMenu>
      </div>
    </div>

    <UCard>
      <template #header>
        <h3 class="font-semibold">Order Items</h3>
      </template>

      <UTable :columns="columns" :rows="order.items" />

      <template #footer>
        <div class="flex justify-end pr-12">
          <div class="text-right">
            <div class="text-sm text-gray-500">Total</div>
            <div class="text-2xl font-bold">{{ order.total }}</div>
          </div>
        </div>
      </template>
    </UCard>
  </div>
</template>
