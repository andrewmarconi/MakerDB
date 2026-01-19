<script setup>
const { data: locations } = await useApiFetch('/inventory/occupancy')
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
      <div v-for="loc in locations" :key="loc.name" class="space-y-2">
        <div class="flex justify-between text-sm">
          <span class="font-medium text-gray-700 dark:text-gray-300">{{ loc.name }}</span>
          <span class="text-gray-500">{{ loc.occupancy }}%</span>
        </div>
        <UProgress :value="loc.occupancy" color="primary" />
      </div>
    </div>

    <template #footer>
      <div class="text-xs text-gray-500">
        Overall utilization: <span class="font-bold">54.2%</span>
      </div>
    </template>
  </UCard>
</template>
