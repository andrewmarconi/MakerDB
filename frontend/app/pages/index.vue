<script setup>
import InventoryValuation from '~/components/Dashboard/InventoryValuation.vue'
import StorageOccupancy from '~/components/Dashboard/StorageOccupancy.vue'
import LowStockAlerts from '~/components/Dashboard/LowStockAlerts.vue'

definePageMeta({
  title: 'Dashboard'
})

const stats = [
  { label: 'Total Parts', value: '1,245', icon: 'i-heroicons-cpu-chip', color: 'text-blue-500' },
  { label: 'Stock Value', value: '$45,230', icon: 'i-heroicons-banknotes', color: 'text-green-500' },
  { label: 'Open Orders', value: '12', icon: 'i-heroicons-shopping-cart', color: 'text-amber-500' },
  { label: 'Active Projects', value: '4', icon: 'i-heroicons-beaker', color: 'text-purple-500' }
]
</script>

<template>
  <div class="space-y-8">
    <!-- Quick Stats -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <UCard v-for="stat in stats" :key="stat.label">
        <div class="flex items-center gap-4">
          <div :class="[stat.color, 'p-2 bg-gray-100 dark:bg-gray-800 rounded-lg']">
            <UIcon :name="stat.icon" class="w-6 h-6" />
          </div>
          <div>
            <div class="text-sm text-gray-500">{{ stat.label }}</div>
            <div class="text-2xl font-bold">{{ stat.value }}</div>
          </div>
        </div>
      </UCard>
    </div>

    <!-- Main Dashboard Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <div class="lg:col-span-2">
        <InventoryValuation />
      </div>
      <div>
        <LowStockAlerts />
      </div>
      <div>
        <StorageOccupancy />
      </div>
      <div class="lg:col-span-2">
        <UCard class="h-full">
          <template #header>
            <h3 class="font-semibold">Recent Activity</h3>
          </template>
          <div class="flex flex-col items-center justify-center p-12 text-gray-400 italic">
            <UIcon name="i-heroicons-clock" class="w-12 h-12 mb-2 opacity-50" />
            Activity feed coming soon...
          </div>
        </UCard>
      </div>
    </div>
  </div>
</template>
