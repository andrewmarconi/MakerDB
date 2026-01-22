<script setup lang="ts">
import InventoryValuation from '~/components/Dashboard/InventoryValuation.vue'
import StorageOccupancy from '~/components/Dashboard/StorageOccupancy.vue'
import LowStockAlerts from '~/components/Dashboard/LowStockAlerts.vue'

definePageMeta({
  title: 'Dashboard'
})

useSeoMeta({
  title: 'Dashboard',
  description: 'View your inventory overview, stock alerts, and recent activity.'
})

const { data: summary } = await useApiFetch('/dashboard/summary')
</script>

<template>
  <div class="space-y-8">
    <!-- Quick Stats -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <UCard>
        <div class="flex items-center gap-4">
          <div class="p-2 bg-blue-100 dark:bg-blue-900/30 rounded-lg">
            <UIcon name="i-heroicons-cpu-chip" class="w-6 h-6 text-blue-500" />
          </div>
          <div>
            <div class="text-sm text-gray-500">Total Parts</div>
            <div class="text-2xl font-bold">{{ summary?.totalParts || 0 }}</div>
          </div>
        </div>
      </UCard>
      <UCard>
        <div class="flex items-center gap-4">
          <div class="p-2 bg-green-100 dark:bg-green-900/30 rounded-lg">
            <UIcon name="i-heroicons-shopping-cart" class="w-6 h-6 text-green-500" />
          </div>
          <div>
            <div class="text-sm text-gray-500">Open Orders</div>
            <div class="text-2xl font-bold">{{ summary?.openOrders || 0 }}</div>
          </div>
        </div>
      </UCard>
      <UCard>
        <div class="flex items-center gap-4">
          <div class="p-2 bg-purple-100 dark:bg-purple-900/30 rounded-lg">
            <UIcon name="i-heroicons-beaker" class="w-6 h-6 text-purple-500" />
          </div>
          <div>
            <div class="text-sm text-gray-500">Active Projects</div>
            <div class="text-2xl font-bold">{{ summary?.activeProjects || 0 }}</div>
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
