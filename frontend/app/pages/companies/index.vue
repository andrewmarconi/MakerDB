<script setup lang="ts">
import type { ColumnDef } from '@tanstack/vue-table'

definePageMeta({
  title: 'Companies'
})

useSeoMeta({
  title: 'Companies',
  description: 'Manage manufacturers and vendors.'
})

interface Company {
  id: string
  name: string
  website: string | null
  is_manufacturer: boolean
  is_vendor: boolean
  created_at: string
}

const columns: ColumnDef<Company>[] = [
  { accessorKey: 'name', header: 'Company Name' },
  { accessorKey: 'website', header: 'Website' },
  { accessorKey: 'is_manufacturer', header: 'Manufacturer' },
  { accessorKey: 'is_vendor', header: 'Vendor' }
]

const cardFields = ['website', 'is_manufacturer', 'is_vendor', 'created_at']

const { data, pending, error } = await useAsyncData(
  'companies',
  (_nuxtApp, { signal }) => $fetch<Company[]>('/db/companies/', { signal }),
)

const isLoading = computed(() => {
  if (pending) return true
  if (error) return true
  return false
})

const showDeleteModal = ref(false)
const companyToDelete = ref<Company | null>(null)
const isDeleting = ref(false)
const deleteError = ref<string | null>(null)

async function handleDelete() {
  if (!companyToDelete.value) return

  isDeleting.value = true
  deleteError.value = null

  try {
    await $fetch(`/core/companies/${companyToDelete.value.id}`, {
      method: 'DELETE'
    })
    showDeleteModal.value = false
    companyToDelete.value = null
    refresh()
  } catch (err: any) {
    deleteError.value = err.data?.detail || err.message || 'Failed to delete company'
  } finally {
    isDeleting.value = false
  }
}

const cardActions = computed(() => [
  {
    label: 'Edit',
    icon: 'i-heroicons-pencil-square',
    onClick: (item: Company) => navigateTo(`/companies/${item.id}/edit`)
  },
  {
    label: 'Delete',
    icon: 'i-heroicons-trash',
    variant: 'destructive' as const,
    onClick: (item: Company) => {
      companyToDelete.value = item
      showDeleteModal.value = true
    }
  }
])
</script>

<template>
  <div class="space-y-6">
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold">Companies</h1>
        <p class="text-gray-500 dark:text-gray-400">Manage manufacturers and vendors.</p>
      </div>
      <div class="flex items-center gap-2">
        <UButton icon="i-heroicons-plus" label="Add Company" color="primary" to="/companies/new" />
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
      v-if="data"
      :data="data as Company[]" 
      :columns="columns" 
      :card-fields="cardFields" 
      :card-actions="cardActions"
      searchable
      clickable-column="name" 
      :default-sort="{ id: 'created_at', desc: true }" 
      :loading="!isLoading"
      :on-row-click="(item) => ({ path: `/companies/${item.id}` })">
      <template #is_manufacturer-cell="{ row }">
        <UIcon 
          :name="row.is_manufacturer ? 'i-heroicons-check-circle' : 'i-heroicons-x-circle'" 
          :class="row.is_manufacturer ? 'text-green-500' : 'text-gray-300'"
          class="w-5 h-5"
        />
      </template>
      <template #is_vendor-cell="{ row }">
        <UIcon 
          :name="row.is_vendor ? 'i-heroicons-check-circle' : 'i-heroicons-x-circle'" 
          :class="row.is_vendor ? 'text-green-500' : 'text-gray-300'"
          class="w-5 h-5"
        />
      </template>
    </DataTable>

    <UModal v-model:open="showDeleteModal">
      <template #header>
        <h3 class="text-lg font-semibold">Delete Company</h3>
      </template>

      <template #body>
        <p class="text-gray-600 dark:text-gray-400">
          Are you sure you want to delete <strong>{{ companyToDelete?.name }}</strong>? This action cannot be undone.
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
