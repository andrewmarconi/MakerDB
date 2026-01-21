<script setup lang="ts">
import type { FieldSchema } from '~/shared/types/ui'
import DataFormView from '~/components/DataFormView.vue'

definePageMeta({
  title: 'Storage Location'
})

useSeoMeta({
  title: 'Storage Location',
  description: 'View and edit storage location details and contents.'
})

const route = useRoute()
const router = useRouter()
const toast = useToast()

// Parse the hierarchical path
const currentPathIds = computed(() => {
  const ids = route.params.id || []
  return Array.isArray(ids) ? ids : [ids]
})

const currentLocationId = computed(() => {
  const ids = currentPathIds.value
  return ids.length > 0 ? ids[ids.length - 1] : null
})

// Fetch current location data (for editing)
const { data: location, refresh: refreshLocation } = await useApiFetch(
  `/inventory/locations/${currentLocationId.value}`,
  { immediate: !!currentLocationId.value }
)

// Fetch all locations (for navigation and parent selection)
const { data: locations, refresh: refreshLocations } = await useApiFetch('/inventory/locations')

// Compute the breadcrumb path
const path = computed(() => {
  const result: any[] = []
  if (!locations.value || !currentLocationId.value) return result

  // Build path from current location upward (if we had parent_id support)
  // For now, just show current location
  const current = locations.value.find((l: any) => l.id === currentLocationId.value)
  if (current) result.push(current)
  return result
})

// Child locations at current level
const childLocations = computed(() => {
  if (!locations.value) return []
  if (!currentLocationId.value) {
    // Top level - show all (no parent filtering since model doesn't have parent_id)
    return locations.value
  }
  // For now, return empty since we don't have hierarchy in the model
  return []
})

// Stock at this location
const { data: allStock } = await useApiFetch('/inventory/stock')

const stockAtLocation = computed(() => {
  if (!allStock.value || !currentLocationId.value) return []
  return allStock.value.filter((s: any) => s.storage?.id === currentLocationId.value)
})

// Schema for DataFormView
const locationSchema: FieldSchema[] = [
  { key: 'name', label: 'Location Name', type: 'text', required: true, span: 2 },
  { key: 'description', label: 'Description', type: 'textarea', span: 2 },
  { key: 'tags', label: 'Tags', type: 'tags', span: 2 },
]

// Handle navigation to child location
function navigateToChild(childId: string) {
  const newPath = [...currentPathIds.value, childId]
  router.push(`/locations/${newPath.join('/')}`)
}

// Handle save events from DataFormView
function handleSave(field: string, value: any, response: any) {
  toast.add({ title: `${field} updated`, icon: 'i-heroicons-check-circle' })
  refreshLocations()
}

function handleSaveError(field: string, error: Error) {
  toast.add({ title: `Failed to update ${field}`, description: error.message, color: 'error' })
}

// Delete functionality
const showDeleteModal = ref(false)
const isDeleting = ref(false)

async function handleDelete() {
  if (!currentLocationId.value) return

  isDeleting.value = true
  try {
    await $fetch(`/db/inventory/locations/${currentLocationId.value}`, { method: 'DELETE' })
    toast.add({ title: 'Location deleted' })
    router.push('/locations')
  } catch (err: any) {
    toast.add({ title: 'Failed to delete', description: err.data?.detail || err.message, color: 'error' })
  } finally {
    isDeleting.value = false
    showDeleteModal.value = false
  }
}
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div class="flex items-center gap-4">
        <UButton
          variant="ghost"
          color="neutral"
          icon="i-heroicons-arrow-left"
          to="/locations"
        />
        <div>
          <h1 class="text-2xl font-bold">
            {{ location?.name || 'Storage Locations' }}
          </h1>
          <LocationBreadcrumbs v-if="path.length > 0" :path="path" class="mt-1" />
        </div>
      </div>
      <div class="flex items-center gap-2">
        <UButton icon="i-heroicons-plus" label="Add Sub-location" color="primary" variant="outline" />
        <LabelPreview
          v-if="location"
          :label="location.name"
          :sublabel="location.description || 'Storage'"
          :id="`LOC-${location.id}`"
        />
        <UButton
          v-if="location"
          icon="i-heroicons-trash"
          color="error"
          variant="ghost"
          @click="showDeleteModal = true"
        />
      </div>
    </div>

    <!-- Location Details Card (with DataFormView for click-to-edit) -->
    <UCard v-if="location">
      <template #header>
        <div class="flex items-center justify-between">
          <h3 class="font-semibold">Location Details</h3>
          <UBadge variant="subtle" color="neutral">
            <UIcon name="i-heroicons-pencil" class="w-3 h-3 mr-1" />
            Click any field to edit
          </UBadge>
        </div>
      </template>

      <DataFormView
        v-model="location"
        :schema="locationSchema"
        endpoint="/inventory/locations"
        :entity-id="currentLocationId!"
        save-mode="put"
        layout="two-column"
        @save="handleSave"
        @save-error="handleSaveError"
      />
    </UCard>

    <!-- Child Locations Grid -->
    <div v-if="childLocations.length > 0">
      <h3 class="text-lg font-semibold mb-4">Sub-locations</h3>
      <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4">
        <UCard
          v-for="child in childLocations"
          :key="child.id"
          class="cursor-pointer hover:ring-2 hover:ring-primary-500 transition-all group"
          @click="navigateToChild(child.id)"
        >
          <div class="flex items-center gap-3">
            <div class="p-2 rounded bg-gray-100 dark:bg-gray-800 text-gray-500 group-hover:bg-primary-50 group-hover:text-primary-600 transition-colors">
              <UIcon name="i-heroicons-archive-box" class="w-6 h-6" />
            </div>
            <div>
              <div class="font-semibold">{{ child.name }}</div>
              <div class="text-xs text-gray-500">{{ child.description || 'No description' }}</div>
            </div>
          </div>
        </UCard>
      </div>
    </div>

    <!-- Empty state for sub-locations when viewing a specific location -->
    <UCard v-else-if="location" class="text-center py-12 bg-gray-50/50 dark:bg-gray-900/50 border-dashed">
      <UIcon name="i-heroicons-archive-box-x-mark" class="w-12 h-12 mx-auto text-gray-300 mb-2" />
      <h3 class="text-lg font-medium text-gray-900 dark:text-white">No sub-locations</h3>
      <p class="text-gray-500">This location has no child locations defined.</p>
      <UButton label="Add First Sub-location" variant="link" color="primary" class="mt-2" />
    </UCard>

    <!-- Stock at this Location -->
    <UCard v-if="location">
      <template #header>
        <div class="flex items-center justify-between">
          <div class="flex flex-col">
            <h3 class="font-semibold">Parts at {{ location.name }}</h3>
            <p class="text-xs text-gray-500">Items physically stored in this location.</p>
          </div>
          <UBadge v-if="stockAtLocation.length > 0" color="primary" variant="subtle">
            {{ stockAtLocation.length }} item{{ stockAtLocation.length !== 1 ? 's' : '' }}
          </UBadge>
        </div>
      </template>

      <div v-if="stockAtLocation.length > 0" class="divide-y divide-gray-200 dark:divide-gray-700">
        <div
          v-for="stock in stockAtLocation"
          :key="stock.id"
          class="flex items-center justify-between py-3 px-2 hover:bg-gray-50 dark:hover:bg-gray-800 rounded"
        >
          <div class="flex items-center gap-3">
            <UIcon name="i-heroicons-cube" class="w-5 h-5 text-gray-400" />
            <div>
              <NuxtLink
                :to="`/inventory/${stock.part_id}`"
                class="font-medium text-primary-600 hover:underline"
              >
                Part #{{ stock.part_id.substring(0, 8) }}...
              </NuxtLink>
              <div v-if="stock.lot" class="text-xs text-gray-500">
                Lot: {{ stock.lot.name }}
              </div>
            </div>
          </div>
          <div class="flex items-center gap-4">
            <div class="text-right">
              <div class="font-semibold">{{ stock.quantity }}</div>
              <div v-if="stock.status" class="text-xs text-gray-500">{{ stock.status }}</div>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="text-sm text-gray-500 italic p-4 text-center">
        No parts currently assigned to this location.
      </div>
    </UCard>

    <!-- Top-level locations list (when no specific location selected) -->
    <div v-if="!currentLocationId && locations">
      <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4">
        <UCard
          v-for="loc in locations"
          :key="loc.id"
          class="cursor-pointer hover:ring-2 hover:ring-primary-500 transition-all group"
          @click="navigateToChild(loc.id)"
        >
          <div class="flex items-center gap-3">
            <div class="p-2 rounded bg-gray-100 dark:bg-gray-800 text-gray-500 group-hover:bg-primary-50 group-hover:text-primary-600 transition-colors">
              <UIcon name="i-heroicons-archive-box" class="w-6 h-6" />
            </div>
            <div>
              <div class="font-semibold">{{ loc.name }}</div>
              <div class="text-xs text-gray-500">{{ loc.description || 'No description' }}</div>
            </div>
          </div>
        </UCard>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <UModal v-model:open="showDeleteModal">
      <template #content>
        <UCard>
          <template #header>
            <h3 class="text-lg font-semibold">Delete Location</h3>
          </template>

          <p class="text-gray-600 dark:text-gray-300">
            Are you sure you want to delete <strong>{{ location?.name }}</strong>?
            This action cannot be undone.
          </p>

          <template #footer>
            <div class="flex items-center justify-end gap-3">
              <UButton label="Cancel" color="neutral" variant="ghost" @click="showDeleteModal = false" />
              <UButton
                label="Delete"
                color="error"
                :loading="isDeleting"
                @click="handleDelete"
              />
            </div>
          </template>
        </UCard>
      </template>
    </UModal>
  </div>
</template>
