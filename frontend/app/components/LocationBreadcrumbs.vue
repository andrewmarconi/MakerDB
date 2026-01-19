<script setup>
const props = defineProps({
  path: {
    type: Array,
    required: true
  }
})

const breadcrumbItems = computed(() => {
  return [
    { label: 'All Locations', to: '/locations', icon: 'i-heroicons-home' },
    ...props.path.map((loc, index) => ({
      label: loc.name,
      to: `/locations/${props.path.slice(0, index + 1).map(l => l.id).join('/')}`
    }))
  ]
})
</script>

<template>
  <UBreadcrumb :items="breadcrumbItems" />
</template>
