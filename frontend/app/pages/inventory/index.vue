<script setup lang="ts">
import { h, resolveComponent } from 'vue'
import type { TableColumn } from '@nuxt/ui'

interface Part {
  id: string
  name: string
  mpn: string
  part_type: string
  total_stock: number
  manufacturer?: { name: string }
}

const UBadge = resolveComponent('UBadge')
const UButton = resolveComponent('UButton')
const UDropdownMenu = resolveComponent('UDropdownMenu')

const columns: TableColumn<Part>[] = [
  {
    accessorKey: 'name',
    header: 'Name',
    enableSorting: true,
    cell: ({ row }) => h('div', { class: 'font-medium' }, row.getValue('name'))
  },
  { accessorKey: 'mpn', header: 'MPN', enableSorting: true },
  {
    accessorKey: 'part_type',
    header: 'Type',
    enableSorting: false,
    cell: ({ row }) => {
      const type = row.getValue('part_type') as string
      const colors: Record<string, string> = {
        'local': 'gray',
        'linked': 'blue',
        'meta': 'purple',
        'sub-assembly': 'green'
      }
      const labels: Record<string, string> = {
        'local': 'Local',
        'linked': 'Linked',
        'meta': 'Meta-Part',
        'sub-assembly': 'Sub-Assembly'
      }
      return h(UBadge, { color: colors[type] || 'gray', variant: 'subtle', size: 'sm' }, () => labels[type] || type || 'Unknown')
    }
  },
  {
    accessorKey: 'total_stock',
    header: 'Stock',
    enableSorting: true,
    cell: ({ row }) => h('div', { class: 'font-mono' }, row.getValue('total_stock'))
  },
  {
    id: 'actions',
    header: '',
    enableSorting: false,
    cell: ({ row }) => {
      const items = [
        { label: 'View Stock', icon: 'i-heroicons-circle-stack' },
        { label: 'Print Label', icon: 'i-heroicons-printer' }
      ]
      return h('div', { class: 'flex justify-end gap-1' }, [
        h(UButton, {
          variant: 'ghost',
          color: 'gray',
          icon: 'i-heroicons-pencil-square',
          to: `/inventory/${row.original.id}`
        }),
        h(UDropdownMenu, { items }, () => {
          return h(UButton, { variant: 'ghost', color: 'gray', icon: 'i-heroicons-ellipsis-horizontal' })
        })
      ])
    }
  }
]

const ITEMS_PER_PAGE = 25
const page = ref(1)
const total = ref(0)
const parts = ref<Part[]>([])
const pending = ref(false)
const search = ref('')
const selectedType = ref('All')
const partTypes = ['All', 'Linked', 'Local', 'Meta', 'Sub-assembly']
const sorting = ref<{ id: string; desc: boolean }[]>([])

async function fetchParts() {
  pending.value = true
  try {
    const skip = (page.value - 1) * ITEMS_PER_PAGE
    let url = `/db/parts/?skip=${skip}&limit=${ITEMS_PER_PAGE}`
    
    if (sorting.value.length > 0) {
      const sort = sorting.value[0]
      const order = sort.desc ? '-' : ''
      url += `&ordering=${order}${sort.id}`
    }

    const [data, countData] = await Promise.all([
      $fetch<Part[]>(url),
      $fetch<{ count: number }>('/db/parts/count')
    ])
    parts.value = Array.isArray(data) ? data : []
    total.value = countData?.count || 0
  } catch (e) {
    console.error('Failed to fetch parts:', e)
    parts.value = []
    total.value = 0
  } finally {
    pending.value = false
  }
}

watch([page, search, selectedType, sorting], () => {
  page.value = 1
  fetchParts()
}, { deep: true })

const filteredItems = computed<Part[]>(() => {
  if (!parts.value) return []
  return (parts.value as Part[]).filter((item: Part) => {
    const matchesSearch = item.name.toLowerCase().includes(search.value.toLowerCase()) ||
      item.mpn.toLowerCase().includes(search.value.toLowerCase())
    const matchesType = selectedType.value === 'All' || item.part_type === selectedType.value.toLowerCase()
    return matchesSearch && matchesType
  })
})

onMounted(fetchParts)
</script>

<template>
  <div class="space-y-6">
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold">Inventory</h1>
        <p class="text-gray-500 dark:text-gray-400">Manage your parts and track stock levels.</p>
      </div>
      <div class="flex items-center gap-2">
        <UButton icon="i-heroicons-plus" label="Add Part" color="primary" to="/inventory/new" />
        <UButton icon="i-heroicons-arrow-up-tray" label="Import" variant="ghost" color="gray" />
      </div>
    </div>

    <UCard>
      <div class="flex flex-col md:flex-row gap-4 mb-4">
        <UInput v-model="search" icon="i-heroicons-magnifying-glass" placeholder="Search Name or MPN..."
          class="flex-1" />
        <USelect v-model="selectedType" :items="partTypes" class="w-48" />
      </div>

      <div v-if="pending" class="flex justify-center py-12">
        <UIcon name="i-heroicons-arrow-path" class="w-8 h-8 animate-spin text-gray-400" />
      </div>

      <div v-else-if="!parts || parts.length === 0" class="text-center py-12 text-gray-500">
        <UIcon name="i-heroicons-circle-stack" class="w-12 h-12 mx-auto mb-4 opacity-50" />
        <p>No parts found.</p>
      </div>

      <UTable v-else :data="filteredItems" :columns="columns" v-model:sorting="sorting" />

      <div v-if="total > ITEMS_PER_PAGE" class="flex justify-center mt-4">
        <UPagination
          v-model:page="page"
          :total="total"
          :items-per-page="ITEMS_PER_PAGE"
          :show-controls="true"
        />
      </div>
    </UCard>
  </div>
</template>
