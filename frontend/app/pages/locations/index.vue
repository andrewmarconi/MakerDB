<script setup lang="ts">
import type { ColumnDef } from '@tanstack/vue-table'

definePageMeta({
  title: 'Storage Locations'
})

useSeoMeta({
  title: 'Storage Locations',
  description: 'Browse and manage your storage hierarchy.'
})

const columns: ColumnDef<InventoryLocation>[] = [
  { accessorKey: 'name', header: 'Location Name' },
  { accessorKey: 'description', header: 'Description' }
]

const cardFields = ['description']

const showDeleteModal = ref(false)
const locationToDelete = ref<InventoryLocation | null>(null)
const isDeleting = ref(false)
const deleteError = ref<string | null>(null)

async function handleDelete() {
  if (!locationToDelete.value) return

  isDeleting.value = true
  deleteError.value = null

  try {
    await $fetch(`/inventory/locations/${locationToDelete.value.id}`, {
      method: 'DELETE'
    })
    showDeleteModal.value = false
    locationToDelete.value = null
  } catch (err: any) {
    deleteError.value = err.data?.detail || err.message || 'Failed to delete location'
  } finally {
    isDeleting.value = false
  }
}

const cardActions = computed(() => [
  {
    label: 'Delete',
    icon: 'i-heroicons-trash',
    variant: 'destructive' as const,
    onClick: (item: InventoryLocation) => {
      locationToDelete.value = item
      showDeleteModal.value = true
    }
  }
])
</script>

<template>
  <DataListView
    model-key="locations"
    :column-defs="columns"
    :card-fields="cardFields"
    :card-actions="cardActions"
    :can-delete="false"
    :default-sort="{ id: 'name', desc: false }"
  />

  <UModal v-model="showDeleteModal">
    <template #content>
      <UCard>
        <template #header>
          <h3 class="text-lg font-semibold">Delete Location</h3>
        </template>

        <p class="text-gray-600 dark:text-gray-400">
          Are you sure you want to delete <strong>{{ locationToDelete?.name }}</strong>? This action cannot be undone.
        </p>
        <UAlert 
          v-if="deleteError" 
          color="error" 
          variant="subtle" 
          icon="i-heroicons-exclamation-circle" 
          class="mt-4"
          :description="deleteError" />

        <template #footer>
          <div class="flex items-center justify-end gap-3">
            <UButton label="Cancel" color="neutral" variant="ghost" @click="showDeleteModal = false" />
            <UButton label="Delete" color="error" :loading="isDeleting" @click="handleDelete" />
          </div>
        </template>
      </UCard>
    </template>
  </UModal>
</template>
