<script setup lang="ts">
import type { tFieldSchema } from '#shared/types/ui'

definePageMeta({
  title: 'Storage Location'
})

useSeoMeta({
  title: 'Storage Location',
  description: 'View and edit storage location details and contents.'
})

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

async function handleStockUpdated(item: any) {
  toast.add({ title: 'Stock updated' })
  await refreshStock()
}

async function handleStockDeleted(id: string) {
  toast.add({ title: 'Stock entry removed' })
  await refreshStock()
}

async function handleStockRefresh() {
  await refreshStock()
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
      <div class="flex items-center gap-2">
        <LabelPreview v-if="location" :label="location.name" :sublabel="location.description || 'Storage'"
          :id="`LOC-${location.id}`" />
        <UButton v-if="location" icon="i-heroicons-trash" color="error" variant="ghost"
          @click="showDeleteModal = true" />
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

          <DataFormView
            v-model="location"
            :schema="detailsSchema"
            endpoint="/inventory/locations"
            :entity-id="currentLocationId!"
            save-mode="put"
            layout="two-column"
            @save="handleSave"
            @save-error="handleSaveError"
          />
        </UCard>
      </template>

      <template #stock>
        <DataFormInlineView
          :items="stockAtLocation || []"
          :item-schema="stockItemSchema"
          :display-columns="stockDisplayColumns"
          :base-endpoint="`/inventory/stock`"
          title="Stock at this Location"
          empty-state-message="No stock at this location."
          @item-updated="handleStockUpdated"
          @item-deleted="handleStockDeleted"
          @refresh="handleStockRefresh"
        />
      </template>
    </UTabs>

    <div v-if="!currentLocationId && locations" class="space-y-4">
      <div class="flex items-center justify-between">
        <h2 class="text-xl font-semibold">Storage Locations</h2>
        <UButton icon="i-heroicons-plus" label="New Location" color="primary" to="/locations/new" />
      </div>
      <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4">
        <UCard v-for="loc in locations" :key="loc.id"
          class="cursor-pointer hover:ring-2 hover:ring-primary-500 transition-all group"
          @click="navigateToChild(loc.id)">
          <div class="flex items-center gap-3">
            <div
              class="p-2 rounded bg-gray-100 dark:bg-gray-800 text-gray-500 group-hover:bg-primary-50 group-hover:text-primary-600 transition-colors">
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
              <UButton label="Delete" color="error" :loading="isDeleting" @click="handleDelete" />
            </div>
          </template>
        </UCard>
      </template>
    </UModal>
  </div>
</template>
