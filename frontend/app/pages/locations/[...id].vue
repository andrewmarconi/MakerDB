<script setup>
const route = useRoute()
const router = useRouter()

const { data: locations, refresh } = await useApiFetch('/inventory/locations')

const currentPathIds = computed(() => {
  const ids = route.params.id || []
  return Array.isArray(ids) ? ids : [ids]
})

const currentLocationId = computed(() => {
  const ids = currentPathIds.value
  return ids.length > 0 ? ids[ids.length - 1] : null
})

const currentLocation = computed(() => {
  if (!locations.value) return null
  return locations.value.find(l => l.id === currentLocationId.value)
})

const path = computed(() => {
  const result = []
  if (!locations.value) return result
  let current = currentLocation.value
  while (current) {
    result.unshift(current)
    const currentParentId = current.parentId // Assuming schema has parent_id or similar
    current = currentParentId ? locations.value.find(l => l.id === currentParentId) : null
  }
  return result
})

const visibleLocations = computed(() => {
  if (!locations.value) return []
  if (!currentLocationId.value) {
    // Top level
    return locations.value.filter(l => !l.parentId)
  }
  return locations.value.filter(l => l.parentId === currentLocationId.value)
})

const navigateTo = (id) => {
  const newPath = [...currentPathIds.value, id]
  router.push(`/locations/${newPath.join('/')}`)
}
</script>

<template>
  <div class="space-y-6">
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold">Storage Locations</h1>
        <LocationBreadcrumbs :path="path" class="mt-1" />
      </div>
      <div class="flex items-center gap-2">
        <UButton icon="i-heroicons-plus" label="Add Location" color="primary" />
        <LabelPreview 
          v-if="currentLocation"
          :label="currentLocation.name" 
          :sublabel="currentLocation.type" 
          :id="`LOC-${currentLocation.id}`" 
        />
      </div>
    </div>

    <div v-if="visibleLocations.length > 0" class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4">
      <UCard
        v-for="loc in visibleLocations"
        :key="loc.id"
        class="cursor-pointer hover:ring-2 hover:ring-primary-500 transition-all group"
        @click="navigateTo(loc.id)"
      >
        <div class="flex items-center gap-3">
          <div class="p-2 rounded bg-gray-100 dark:bg-gray-800 text-gray-500 group-hover:bg-primary-50 group-hover:text-primary-600 transition-colors">
            <UIcon :name="loc.type === 'Room' ? 'i-heroicons-home' : (loc.type === 'Shelf' ? 'i-heroicons-square-3-stack-3d' : 'i-heroicons-archive-box')" class="w-6 h-6" />
          </div>
          <div>
            <div class="font-semibold">{{ loc.name }}</div>
            <div class="text-xs text-gray-500 capitalize">{{ loc.type }}</div>
          </div>
        </div>
      </UCard>
    </div>

    <UCard v-else-if="currentLocation" class="text-center py-12 bg-gray-50/50 dark:bg-gray-900/50 border-dashed">
      <UIcon name="i-heroicons-archive-box-x-mark" class="w-12 h-12 mx-auto text-gray-300 mb-2" />
      <h3 class="text-lg font-medium text-gray-900 dark:text-white">No sub-locations</h3>
      <p class="text-gray-500">This location has no child locations defined.</p>
      <UButton label="Add First Sub-location" variant="link" color="primary" class="mt-2" />
    </UCard>

    <!-- Parts in this location -->
    <UCard v-if="currentLocation" class="mt-8">
      <template #header>
        <div class="flex flex-col">
          <h3 class="font-semibold">Parts at {{ currentLocation.name }}</h3>
          <p class="text-xs text-gray-500">Items physically stored in this exact container.</p>
        </div>
      </template>
      
      <div class="text-sm text-gray-500 italic p-4">
        No parts currently assigned to this location.
      </div>
    </UCard>
  </div>
</template>
