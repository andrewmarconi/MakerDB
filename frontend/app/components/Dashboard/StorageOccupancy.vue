<script setup>
const { data: occupancy } = await useApiFetch('/inventory/occupancy')
</script>

<template>
  <UCard class="h-full">
    <template #header>
      <div class="flex items-center justify-between">
        <h3 class="font-semibold text-gray-900 dark:text-white">Storage Occupancy</h3>
        <UIcon name="i-heroicons-archive-box" class="text-primary-500 w-5 h-5" />
      </div>
    </template>

    <div class="space-y-6">
      <div class="text-center">
        <div class="text-4xl font-bold" :class="occupancy?.used_percentage > 80 ? 'text-orange-500' : 'text-primary-500'">
          {{ occupancy?.used_percentage || 0 }}%
        </div>
        <div class="text-sm text-gray-500 mt-1">Storage locations in use</div>
        <div class="text-xs text-gray-400 mt-2">
          {{ occupancy?.used_locations || 0 }} of {{ occupancy?.total_locations || 0 }} locations have items
        </div>
      </div>

      <div v-if="occupancy?.top_locations?.length" class="space-y-3">
        <div class="text-xs font-medium text-gray-500 uppercase tracking-wide">Top Locations</div>
        <div v-for="loc in occupancy.top_locations" :key="loc.name" class="flex items-center justify-between text-sm">
          <span class="text-gray-700 dark:text-gray-300 truncate pr-2">{{ loc.name }}</span>
          <span class="font-mono text-gray-500">{{ loc.quantity }}</span>
        </div>
      </div>
    </div>

    <template #footer>
      <div class="text-xs text-gray-500">
        <span class="font-bold">{{ occupancy?.empty_locations || 0 }}</span> empty locations available
      </div>
    </template>
  </UCard>
</template>
