<script setup lang="ts">
import type { tFieldSchema } from '#shared/types/ui'

const route = useRoute()
const router = useRouter()
const toast = useToast()

const locationId = route.params.id as string
const isRoot = !locationId || locationId === ''

const tabs = [
  { key: 'details', slot: 'details', label: 'Details', icon: 'i-heroicons-information-circle' },
  { key: 'stock', slot: 'stock', label: 'Stock', icon: 'i-heroicons-circle-stack' }
]
const activeTab = ref('details')

const { data: location, refresh: refreshLocation } = isRoot ? ref(null) : await useApiFetch(`/inventory/locations/${locationId}`)
const { data: stockAtLocation, refresh: refreshStock } = isRoot ? ref([]) : await useApiFetch(`/inventory/stock`, { query: { location_id: locationId } })
const { data: locations } = isRoot ? await useApiFetch('/inventory/locations') : ref(null)

const showDeleteModal = ref(false)
const isDeleting = ref(false)

const detailsSchema: tFieldSchema[] = [
  { key: 'name', label: 'Location Name', type: 'text', required: true },
  { key: 'description', label: 'Description', type: 'textarea', span: 2 }
]

const stockItemSchema: tFieldSchema[] = [
  { key: 'quantity', label: 'Qty', type: 'number', required: true },
  {
    key: 'status', label: 'Status', type: 'select', options: [
      { label: 'Available', value: 'available' },
      { label: 'Reserved', value: 'reserved' },
      { label: 'Allocated', value: 'allocated' },
      { label: 'Ordered', value: 'ordered' },
    ]
  },
]

const stockDisplayColumns = [
  {
    key: 'part',
    label: 'Part',
    render: (item: any) => {
      if (!item.part) return h('span', { class: 'text-gray-400' }, '-')
      return h(NuxtLink, { to: `/inventory/${item.part.id}`, class: 'text-primary-500 hover:underline font-medium' }, () => item.part.name)
    }
  },
  {
    key: 'part_mpn',
    label: 'MPN',
    render: (item: any) => {
      if (!item.part?.mpn) return '-'
      return h('span', { class: 'font-mono text-gray-500 text-sm' }, item.part.mpn)
    }
  },
  {
    key: 'lot',
    label: 'Lot',
    render: (item: any) => {
      if (!item.lot) return '-'
      return h('span', { class: 'text-sm' }, item.lot.name)
    }
  },
]

async function handleSave() {
  toast.add({ title: 'Location updated' })
  await refreshLocation()
}

async function handleSaveError(err: any) {
  toast.add({ title: 'Failed to update', description: err.message, color: 'error' })
}

async function handleStockUpdated() {
  toast.add({ title: 'Stock updated' })
  await refreshStock()
}

async function handleStockDeleted() {
  toast.add({ title: 'Stock entry removed' })
  await refreshStock()
}

async function handleStockRefresh() {
  await refreshStock()
}

async function handleDelete() {
  if (!location) return

  isDeleting.value = true
  try {
    await $fetch(`/inventory/locations/${locationId}`, { method: 'DELETE' })
    toast.add({ title: 'Location deleted' })
    router.push('/locations')
  } catch (err: any) {
    toast.add({ title: 'Failed to delete', description: err.message, color: 'error' })
  } finally {
    isDeleting.value = false
  }
}

function navigateToChild(id: string) {
  router.push(`/locations/${id}`)
}
</script>

<template>
  <div class="space-y-6">
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div class="flex items-center gap-4">
        <UButton variant="ghost" color="neutral" icon="i-heroicons-arrow-left" to="/locations" />
        <div>
          <h1 class="text-2xl font-bold">
            {{ location?.name || 'Storage Locations' }}
          </h1>
        </div>
      </div>
      <div v-if="location" class="flex items-center gap-2">
        <LabelPreview :label="location.name" :sublabel="location.description || 'Storage'" :id="`LOC-${location.id}`" />
        <UButton icon="i-heroicons-trash" color="error" variant="ghost" @click="showDeleteModal = true" />
      </div>
    </div>

    <UTabs v-model="activeTab" :items="tabs" class="w-full">
      <template #details>
        <UCard>
          <template #header>
            <div class="flex items-center justify-between">
              <h3 class="font-semibold">Location Details</h3>
              <UBadge variant="subtle" color="neutral">
                <UIcon name="i-heroicons-pencil" class="w-3 h-3 mr-1" />
                Click any field to edit
              </UBadge>
            </div>
          </template>

          <DataFormView v-model="location" :schema="detailsSchema" endpoint="/inventory/locations"
            :entity-id="currentLocationId!" save-mode="put" layout="two-column" @save="handleSave"
            @save-error="handleSaveError" />
        </UCard>
      </template>
      <template #stock>
        <DataFormInlineView :items="stockAtLocation || []" :item-schema="stockItemSchema"
          :display-columns="stockDisplayColumns" :base-endpoint="`/inventory/stock`" title="Stock at this Location"
          empty-state-message="No stock at this location." @item-updated="handleStockUpdated"
          @item-deleted="handleStockDeleted" @refresh="handleStockRefresh" />
      </template>
    </UTabs>


    <UModal v-model:open="showDeleteModal">
      <template #body>
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
              <UButton label="Delete" color="error" :loading="isDeleting" @click="handleDelete" />
            </div>
          </template>
        </UCard>
      </template>
    </UModal>
  </div>
</template>
