<script setup>
// Root locations view - show all top-level storage locations
const { data: locations, error, refresh } = await useApiFetch('/inventory/locations')

// Delete functionality
const showDeleteModal = ref(false)
const locationToDelete = ref(null)
const isDeleting = ref(false)
const deleteError = ref(null)

function confirmDelete(location) {
  locationToDelete.value = location
  showDeleteModal.value = true
  deleteError.value = null
}

async function handleDelete() {
  if (!locationToDelete.value) return

  isDeleting.value = true
  deleteError.value = null

  try {
    await useApiFetch(`/inventory/locations/${locationToDelete.value.id}`, {
      method: 'DELETE'
    })
    showDeleteModal.value = false
    locationToDelete.value = null
    refresh()
  } catch (err) {
    deleteError.value = err.message || 'Failed to delete location. It may contain stock entries.'
  } finally {
    isDeleting.value = false
  }
}

// Dropdown menu items for each location
function getLocationActions(location) {
  return [
    [
      { label: 'Edit', icon: 'i-heroicons-pencil-square', to: `/locations/${location.id}/edit` },
      { label: 'View Details', icon: 'i-heroicons-eye', to: `/locations/${location.id}` }
    ],
    [
      { label: 'Delete', icon: 'i-heroicons-trash', color: 'error', onSelect: () => confirmDelete(location) }
    ]
  ]
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
        <UButton icon="i-heroicons-plus" label="Add Location" color="primary" to="/locations/new" />
      </div>
    </div>

    <UCard>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div v-for="location in locations" :key="location.id"
          class="p-4 border border-gray-200 dark:border-gray-800 rounded-lg hover:border-primary-500 dark:hover:border-primary-400 transition-colors group">
          <div class="flex items-start justify-between">
            <NuxtLink :to="`/locations/${location.id}`" class="flex-1">
              <h3 class="font-semibold text-lg group-hover:text-primary-500">{{ location.name }}</h3>
              <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">{{ location.description || 'No description' }}</p>
            </NuxtLink>
            <UDropdownMenu :items="getLocationActions(location)">
              <UButton variant="ghost" color="gray" icon="i-heroicons-ellipsis-vertical" size="sm" />
            </UDropdownMenu>
          </div>
          <div class="mt-3 flex items-center gap-4 text-sm text-gray-600 dark:text-gray-400">
            <span v-if="location.children_count">
              <UIcon name="i-heroicons-folder" class="w-4 h-4 inline mr-1" />
              {{ location.children_count }} sub-locations
            </span>
          </div>
        </div>
      </div>

      <div v-if="error" class="text-center py-12 text-red-500">
        <UIcon name="i-heroicons-exclamation-triangle" class="w-12 h-12 mx-auto mb-4" />
        <p class="font-semibold">Failed to load storage locations</p>
        <p class="text-sm mt-2 text-gray-500">{{ error.message || 'An error occurred' }}</p>
      </div>

      <div v-else-if="!locations || locations.length === 0" class="text-center py-12 text-gray-500">
        <UIcon name="i-heroicons-folder-open" class="w-12 h-12 mx-auto mb-4 opacity-50" />
        <p class="mb-4">No storage locations found. Create one to get started.</p>
        <UButton icon="i-heroicons-plus" label="Create First Location" color="primary" to="/locations/new" />
      </div>
    </UCard>

    <!-- Delete Confirmation Modal -->
    <UModal v-model:open="showDeleteModal" title="Delete Location">
      <template #body>
        <p class="text-gray-600 dark:text-gray-400">
          Are you sure you want to delete <strong>{{ locationToDelete?.name }}</strong>? This action cannot be undone.
        </p>
        <UAlert v-if="deleteError" color="error" variant="subtle" icon="i-heroicons-exclamation-circle" class="mt-4"
          :description="deleteError" />
      </template>

      <template #footer>
        <div class="flex items-center justify-end gap-3">
          <UButton label="Cancel" color="gray" variant="ghost" @click="showDeleteModal = false" />
          <UButton label="Delete" color="error" :loading="isDeleting" @click="handleDelete" />
        </div>
      </template>
    </UModal>
  </div>
</template>
