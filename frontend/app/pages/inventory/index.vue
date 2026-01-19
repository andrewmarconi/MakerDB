<script setup>
const columns = [
  { id: 'name', key: 'name', label: 'Name', sortable: true },
  { id: 'mpn', key: 'mpn', label: 'MPN', sortable: true },
  { id: 'type', key: 'type', label: 'Type' },
  { id: 'stock', key: 'stock', label: 'Stock', sortable: true },
  { id: 'price', key: 'price', label: 'Price', sortable: true },
  { id: 'actions', key: 'actions', label: '' }
]

const { data: parts, refresh } = await useApiFetch('/parts/')

const search = ref('')
const selectedType = ref('All')
const partTypes = ['All', 'Linked', 'Local', 'Meta', 'Sub-assembly']

const filteredItems = computed(() => {
  if (!parts.value) return []
  return parts.value.filter(item => {
    const matchesSearch = item.name.toLowerCase().includes(search.value.toLowerCase()) ||
      item.mpn.toLowerCase().includes(search.value.toLowerCase())
    const matchesType = selectedType.value === 'All' || item.part_type === selectedType.value.toLowerCase()
    return matchesSearch && matchesType
  })
})
</script>

<template>
  <div class="space-y-6">
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold">Inventory</h1>
        <p class="text-gray-500 dark:text-gray-400">Manage your parts and track stock levels.</p>
      </div>
      <div class="flex items-center gap-2">
        <UButton icon="i-heroicons-plus" label="Add Part" color="primary" />
        <UButton icon="i-heroicons-arrow-up-tray" label="Import" variant="ghost" color="gray" />
      </div>
    </div>

    <UCard>
      <div class="flex flex-col md:flex-row gap-4 mb-4">
        <UInput v-model="search" icon="i-heroicons-magnifying-glass" placeholder="Search Name or MPN..."
          class="flex-1" />
        <USelect v-model="selectedType" :options="partTypes" class="w-48" />
      </div>

      <UTable :columns="columns" :rows="filteredItems">
        <template #type-data="{ row }">
          <StatusBadge :status="row.type" />
        </template>

        <template #stock-data="{ row }">
          <div class="font-mono">{{ row.stock }}</div>
        </template>

        <template #actions-data="{ row }">
          <div class="flex justify-end">
            <UButton variant="ghost" color="gray" icon="i-heroicons-pencil-square" :to="`/inventory/${row.id}`" />
            <UDropdownMenu
              :items="[[{ label: 'View Stock', icon: 'i-heroicons-circle-stack' }, { label: 'Print Label', icon: 'i-heroicons-printer' }]]">
              <UButton variant="ghost" color="gray" icon="i-heroicons-ellipsis-horizontal" />
            </UDropdownMenu>
          </div>
        </template>
      </UTable>
    </UCard>
  </div>
</template>
