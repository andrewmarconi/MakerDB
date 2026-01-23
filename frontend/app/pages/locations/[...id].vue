<script setup lang="ts">
import type { tFieldSchema } from '#shared/types/ui'

const route = useRoute()
const router = useRouter()
const toast = useToast()

const locationId = (Array.isArray(route.params.id) ? route.params.id[0] : route.params.id) || ''
const isRoot = !locationId || locationId === ''

const tabs = [
  { key: 'details', slot: 'details', label: 'Details', icon: 'i-heroicons-information-circle' },
  { key: 'stock', slot: 'stock', label: 'Stock', icon: 'i-heroicons-circle-stack' }
]
// const activeTab = ref('details')

const { data: location, refresh: refreshLocation } = isRoot ? ref(null) : await useApiFetch(`/inventory/locations/${locationId}`)
const { data: stockAtLocation, refresh: refreshStock } = isRoot ? ref([]) : await useApiFetch(`/inventory/locations/${locationId}/stock`)
const { data: locations } = isRoot ? await useApiFetch('/inventory/locations') : ref(null)

const showDeleteModal = ref(false)
const isDeleting = ref(false)

const detailsSchema: tFieldSchema[] = [
  { key: 'name', label: 'Location Name', type: 'text', required: true },
  { key: 'description', label: 'Description', type: 'textarea', span: 2 }
]

const stockDisplayColumns = [
  { accessorKey: 'part.name', header: 'Part' },
  { accessorKey: 'part.mpn', header: 'MPN' },
  { accessorKey: 'totalQuantity', header: 'Quantity' },
]

// Group stock entries by part
const groupedStock = computed(() => {
  if (!stockAtLocation.value || stockAtLocation.value.length === 0) return []

  const grouped = new Map()

  for (const stock of stockAtLocation.value) {
    if (!stock.part) continue

    const partId = stock.part.id

    if (grouped.has(partId)) {
      // Add to existing group
      const existing = grouped.get(partId)
      existing.totalQuantity += stock.quantity || 0
    } else {
      // Create new group
      grouped.set(partId, {
        id: partId,
        part: stock.part,
        totalQuantity: stock.quantity || 0
      })
    }
  }

  return Array.from(grouped.values())
})

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

    <UTabs :items="tabs" class="w-full">
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
            :entity-id="locationId" save-mode="put" layout="two-column" @save="handleSave"
            @save-error="handleSaveError" />
        </UCard>
      </template>
      <template #stock>
        <UCard>
          <template #header>
            <h3 class="font-semibold">Stock at this Location</h3>
          </template>

          <div v-if="groupedStock.length === 0" class="text-center py-8 text-gray-500">
            No stock at this location.
          </div>

          <UTable v-else :data="groupedStock" :columns="stockDisplayColumns">
            <template #part.name-cell="{ row, getValue }">
              <NuxtLink v-if="row.original.part" :to="`/inventory/${row.original.part.id}`" class="text-primary-500 hover:underline font-medium">
                {{ getValue() }}
              </NuxtLink>
              <span v-else class="text-gray-400">-</span>
            </template>
            <template #part.mpn-cell="{ row, getValue }">
              <span v-if="row.original.part?.mpn" class="font-mono text-gray-500 text-sm">{{ getValue() }}</span>
              <span v-else class="text-gray-400">-</span>
            </template>
          </UTable>
        </UCard>
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
