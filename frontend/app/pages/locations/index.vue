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
  { accessorKey: 'description', header: 'Description' },
  { accessorKey: 'children_count', header: 'Sub-locations' },
  { accessorKey: 'created_at', header: 'Created' }
]

const cardFields = ['description', 'children_count', 'created_at']

const { data, pending, error, refresh } = await useAsyncData(
  'locations',
  (_nuxtApp, { signal }) => $fetch<InventoryLocation[]>('/db/inventory/locations/', { signal }),
)

const isLoading = computed(() => pending.value || !!error.value)

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
    refresh()
  } catch (err: any) {
    deleteError.value = err.data?.detail || err.message || 'Failed to delete location'
  } finally {
    isDeleting.value = false
  }
}

const cardActions = computed(() => [
  {
    label: 'Edit',
    icon: 'i-heroicons-pencil-square',
    onClick: (item: InventoryLocation) => navigateTo(`/locations/${item.id}/edit`)
  },
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
  <div class="space-y-6">
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold">Storage InventoryLocations</h1>
        <p class="text-gray-500 dark:text-gray-400">Browse and manage your storage hierarchy.</p>
      </div>
      <div class="flex items-center gap-2">
        <UButton icon="i-heroicons-plus" label="Add Location" color="primary" to="/locations/new" />
      </div>
    </div>
    <template v-if="error">
      <UAlert 
        color="error"
        title="There was a problem loading data"
        :description="error.message"
        icon="i-lucide-terminal"
      />
    </template>
    <DataTable 
      :data="(data || []) as InventoryLocation[]" 
      :columns="columns" 
      :card-fields="cardFields" 
      :card-actions="cardActions"
      searchable
      clickable-column="name" 
      :default-sort="{ id: 'name', desc: false }" 
      :loading="isLoading"
      :on-row-click="(item) => ({ path: `/locations/${item.id}` })">
      <template #children_count-cell="{ row }">
        <div class="flex items-center gap-1">
          <UIcon name="i-heroicons-folder" class="w-4 h-4 text-warning" />
          <span>{{ row.children_count }} sub-locations</span>
        </div>
      </template>
    </DataTable>

    <UModal v-model:open="showDeleteModal">
      <template #header>
        <h3 class="text-lg font-semibold">Delete Location</h3>
      </template>

      <template #body>
        <p class="text-gray-600 dark:text-gray-400">
          Are you sure you want to delete <strong>{{ locationToDelete?.name }}</strong>? This action cannot be undone.
        </p>
        <UAlert v-if="deleteError" color="error" variant="subtle" icon="i-heroicons-exclamation-circle" class="mt-4"
          :description="deleteError" />
      </template>

      <template #footer>
        <div class="flex items-center justify-end gap-3">
          <UButton label="Cancel" color="neutral" variant="ghost" @click="showDeleteModal = false" />
          <UButton label="Delete" color="error" :loading="isDeleting" @click="handleDelete" />
        </div>
      </template>
    </UModal>
  </div>
</template>
