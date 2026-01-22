<script setup lang="ts">
const { data: stats } = await useApiFetch('/dashboard/stats') // Assuming a stats endpoint

const totalValue = computed(() => stats.value?.inventoryValue || 0)
const currency = computed(() => stats.value?.currency || 'USD')
const trends = computed(() => stats.value?.valueTrends || [0,0,0,0,0,0,0])

const formattedValue = computed(() => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: currency.value
  }).format(totalValue.value)
})
</script>

<template>
  <UCard class="h-full">
    <template #header>
      <div class="flex items-center justify-between">
        <h3 class="font-semibold text-gray-900 dark:text-white">Inventory Valuation</h3>
        <UIcon name="i-heroicons-banknotes" class="text-primary-500 w-5 h-5" />
      </div>
    </template>

    <div class="space-y-4">
      <div>
        <div class="text-3xl font-bold">{{ formattedValue }}</div>
        <div class="text-sm text-green-500 flex items-center gap-1 mt-1">
          <UIcon name="i-heroicons-arrow-trending-up" />
          <span>+4.2% from last month</span>
        </div>
      </div>

      <!-- Simple Sparkline Mock -->
      <div class="h-16 flex items-end gap-1 pt-4">
        <div 
          v-for="(val, i) in trends" 
          :key="i"
          class="flex-1 bg-primary-500/20 hover:bg-primary-500 transition-colors rounded-t-sm"
          :style="{ height: `${(val / Math.max(...trends)) * 100}%` }"
        />
      </div>
    </div>

    <template #footer>
      <div class="flex justify-between text-xs text-gray-500">
        <span>Active Inventory</span>
        <span>1,245 Parts</span>
      </div>
    </template>
  </UCard>
</template>
