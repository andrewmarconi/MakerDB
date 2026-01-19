<script setup>
const stats = [
  { label: 'Total Parts', value: '1,234' },
  { label: 'Stock Value', value: '$45,678' },
  { label: 'Active Projects', value: '12' },
  { label: 'Open Orders', value: '5' }
]
</script>

<template>
  <div class="space-y-6">
    <UPageHeader title="Welcome to MakerDB" description="Manage your electronics production from inventory to BOM pricing." />

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <UCard v-for="stat in stats" :key="stat.label">
        <template #header>
          <div class="text-sm font-medium text-gray-500 dark:text-gray-400">{{ stat.label }}</div>
        </template>
        <div class="text-2xl font-bold">{{ stat.value }}</div>
      </UCard>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <UCard>
        <template #header>
          <h3 class="font-semibold">Recent Build Activity</h3>
        </template>
        <div class="text-sm text-gray-500 italic">No recent activity found.</div>
      </UCard>

      <UCard>
        <template #header>
          <h3 class="font-semibold">Low Stock Alerts</h3>
        </template>
        <div class="text-sm text-gray-500 italic">Everything is in stock!</div>
      </UCard>
    </div>
  </div>
</template>
