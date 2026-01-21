<script setup>
const { data: alerts } = await useApiFetch('/inventory/low-stock')
</script>

<template>
  <UCard class="h-full">
    <template #header>
      <div class="flex items-center justify-between">
        <h3 class="font-semibold text-gray-900 dark:text-white">Low Stock Alerts</h3>
        <UIcon name="i-heroicons-bell-alert" class="text-red-500 w-5 h-5 animate-pulse" />
      </div>
    </template>

    <div class="divide-y divide-gray-100 dark:divide-gray-800">
      <div v-for="alert in alerts" :key="alert.id" class="py-3 flex items-center justify-between group cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-900/50 transition-colors px-2 rounded-lg -mx-2">
        <div class="min-w-0 flex-1">
          <div class="flex items-center gap-2">
            <span class="text-sm font-medium truncate">{{ alert.name }}</span>
            <UBadge :color="alert.status === 'Critical' ? 'error' : 'warning'" size="xs" variant="subtle">
              {{ alert.status }}
            </UBadge>
          </div>
          <div class="text-xs text-gray-500 font-mono">{{ alert.mpn }}</div>
        </div>
        <div class="text-right ml-4">
          <div class="text-sm font-bold" :class="alert.status === 'Critical' ? 'text-red-500' : 'text-orange-500'">
            {{ alert.stock }}
          </div>
          <div class="text-[10px] text-gray-400">Min: {{ alert.min }}</div>
        </div>
      </div>
    </div>

    <template #footer>
      <UButton label="View all alerts" variant="link" color="neutral" size="sm" block />
    </template>
  </UCard>
</template>
