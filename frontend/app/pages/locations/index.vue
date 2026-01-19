<script setup>
// Root locations view - show all top-level storage locations
const { data: locations, error, refresh } = await useApiFetch('/inventory/locations')

const isModalOpen = ref(false)
const formData = ref({
  name: '',
  description: '',
  parent: null
})

const handleSubmit = async () => {
  try {
    await useApiFetch('/inventory/locations', {
      method: 'POST',
      body: formData.value
    })
    isModalOpen.value = false
    formData.value = { name: '', description: '', parent: null }
    refresh()
  } catch (err) {
    console.error('Failed to create location:', err)
  }
}
</script>

<template>
  <div class="space-y-6">
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold">Storage Locations</h1>
        <p class="text-gray-500 dark:text-gray-400">Browse and manage your storage hierarchy.</p>
      </div>
      <div class="flex items-center gap-2">
        <UButton icon="i-heroicons-plus" label="Add Location" color="primary" />
      </div>
    </div>

    <UCard>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <NuxtLink v-for="location in locations" :key="location.id" :to="`/locations/${location.id}`"
          class="p-4 border border-gray-200 dark:border-gray-800 rounded-lg hover:border-primary-500 dark:hover:border-primary-400 transition-colors">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <h3 class="font-semibold text-lg">{{ location.name }}</h3>
              <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">{{ location.description || 'No description' }}
              </p>
            </div>
            <UIcon name="i-heroicons-chevron-right" class="w-5 h-5 text-gray-400" />
          </div>
          <div class="mt-3 flex items-center gap-4 text-sm text-gray-600 dark:text-gray-400">
            <span v-if="location.children_count">
              <UIcon name="i-heroicons-folder" class="w-4 h-4 inline mr-1" />
              {{ location.children_count }} sub-locations
            </span>
          </div>
        </NuxtLink>
      </div>

      <div v-if="error" class="text-center py-12 text-red-500">
        <UIcon name="i-heroicons-exclamation-triangle" class="w-12 h-12 mx-auto mb-4" />
        <p class="font-semibold">Failed to load storage locations</p>
        <p class="text-sm mt-2 text-gray-500">{{ error.message || 'An error occurred' }}</p>
      </div>

      <div v-else-if="!locations || locations.length === 0" class="text-center py-12 text-gray-500">
        <UIcon name="i-heroicons-folder-open" class="w-12 h-12 mx-auto mb-4 opacity-50" />
        <p>No storage locations found. Create one to get started.</p>
      </div>
    </UCard>
  </div>
</template>
