<script setup lang="ts">
const route = useRoute()
const router = useRouter()

const locationId = computed(() => route.params.id as string)

// Fetch location data
const { data: location, error: fetchError, refresh } = await useApiFetch(`/inventory/locations/${locationId.value}`)

// Fetch all locations for parent selection
const { data: locations } = await useApiFetch('/inventory/locations')

const parentOptions = computed(() => {
  if (!locations.value) return [{ label: 'None (Top Level)', value: null }]
  // Exclude current location from parent options
  return [
    { label: 'None (Top Level)', value: null },
    ...locations.value
      .filter((loc: any) => loc.id !== locationId.value)
      .map((loc: any) => ({ label: loc.name, value: loc.id }))
  ]
})

// Form state
const form = ref({
  name: '',
  description: '',
  parent_id: null as string | null
})

// Initialize form with location data
watchEffect(() => {
  if (location.value) {
    form.value = {
      name: location.value.name || '',
      description: location.value.description || '',
      parent_id: location.value.parent_id || null
    }
  }
})

// Submission
const isSubmitting = ref(false)
const error = ref<string | null>(null)

async function handleSubmit() {
  isSubmitting.value = true
  error.value = null

  try {
    await useApiFetch(`/inventory/locations/${locationId.value}`, {
      method: 'PUT',
      body: {
        name: form.value.name,
        description: form.value.description
      }
    })

    router.push('/locations')
  } catch (err: any) {
    error.value = err.message || 'Failed to update location'
  } finally {
    isSubmitting.value = false
  }
}

// Delete functionality
const showDeleteModal = ref(false)
const isDeleting = ref(false)

async function handleDelete() {
  isDeleting.value = true
  error.value = null

  try {
    await useApiFetch(`/inventory/locations/${locationId.value}`, {
      method: 'DELETE'
    })

    router.push('/locations')
  } catch (err: any) {
    error.value = err.message || 'Failed to delete location'
    showDeleteModal.value = false
  } finally {
    isDeleting.value = false
  }
}

// Validation
const isValid = computed(() => form.value.name.trim().length > 0)
</script>

<template>
  <div class="max-w-2xl mx-auto space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold">Edit Location</h1>
        <p class="text-gray-500 dark:text-gray-400">Update storage location details.</p>
      </div>
      <UButton icon="i-heroicons-x-mark" variant="ghost" color="gray" to="/locations" />
    </div>

    <!-- Fetch Error -->
    <UAlert v-if="fetchError" color="error" variant="subtle" icon="i-heroicons-exclamation-circle"
      title="Failed to load location" :description="fetchError.message || 'An error occurred'" />

    <!-- Edit Form -->
    <UCard v-else-if="location">
      <template #header>
        <h3 class="font-semibold">Location Details</h3>
      </template>

      <div class="space-y-4">
        <UFormField label="Name" required>
          <UInput v-model="form.name" placeholder="Location name" class="w-full" />
        </UFormField>

        <UFormField label="Description">
          <UTextarea v-model="form.description" placeholder="Optional description..." class="w-full" :rows="3" />
        </UFormField>

        <UFormField label="Parent Location">
          <USelect v-model="form.parent_id" :items="parentOptions" value-key="value" class="w-full" />
        </UFormField>
      </div>

      <template #footer>
        <div class="flex items-center justify-between">
          <UButton label="Delete Location" color="error" variant="ghost" icon="i-heroicons-trash"
            @click="showDeleteModal = true" />

          <div class="flex items-center gap-3">
            <UButton label="Cancel" color="gray" variant="ghost" to="/locations" />
            <UButton label="Save Changes" color="primary" :loading="isSubmitting" :disabled="!isValid || isSubmitting"
              @click="handleSubmit" />
          </div>
        </div>
      </template>
    </UCard>

    <!-- Loading State -->
    <UCard v-else>
      <div class="flex items-center justify-center py-12">
        <UIcon name="i-heroicons-arrow-path" class="w-8 h-8 animate-spin text-gray-400" />
      </div>
    </UCard>

    <!-- Error Display -->
    <UAlert v-if="error" color="error" variant="subtle" icon="i-heroicons-exclamation-circle" title="Error"
      :description="error" />

    <!-- Delete Confirmation Modal -->
    <UModal v-model:open="showDeleteModal" title="Delete Location" description="Are you sure you want to delete this location? This action cannot be undone.">
      <template #footer>
        <div class="flex items-center justify-end gap-3">
          <UButton label="Cancel" color="gray" variant="ghost" @click="showDeleteModal = false" />
          <UButton label="Delete" color="error" :loading="isDeleting" @click="handleDelete" />
        </div>
      </template>
    </UModal>
  </div>
</template>
