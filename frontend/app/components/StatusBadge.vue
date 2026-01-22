<script setup lang="ts">
const props = defineProps({
  status: {
    type: String,
    required: true
  },
  type: {
    type: String,
    default: 'default' // 'inventory', 'order', 'project'
  }
})

const colorMap = {
  // Inventory/Parts
  'Linked': 'blue',
  'Local': 'orange',
  'Meta': 'purple',
  'Sub-assembly': 'green',
  
  // Orders
  'Open': 'blue',
  'Ordered': 'yellow',
  'Received': 'green',
  
  // Project
  'Draft': 'gray',
  'Active': 'primary',
  'Completed': 'green',
  'Archived': 'gray',
  
  // Stock
  'In Stock': 'green',
  'Low Stock': 'orange',
  'Out of Stock': 'red'
}

const color = computed(() => colorMap[props.status] || 'gray')
</script>

<template>
  <UBadge
    :color="color"
    variant="subtle"
    class="capitalize font-medium"
  >
    {{ status }}
  </UBadge>
</template>
