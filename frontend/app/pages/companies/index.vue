<script setup lang="ts">
definePageMeta({
  title: 'Companies'
})

const router = useRouter()
const toast = useToast()

const { data: companies, refresh } = await useApiFetch('/core/companies')

const searchQuery = ref('')
const typeFilter = ref<'all' | 'manufacturer' | 'vendor'>('all')

const filteredCompanies = computed(() => {
  if (!companies.value) return []

  return (companies.value as any[]).filter((company: any) => {
    const matchesSearch = company.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesType = typeFilter.value === 'all' ||
      (typeFilter.value === 'manufacturer' && company.is_manufacturer) ||
      (typeFilter.value === 'vendor' && company.is_vendor)
    return matchesSearch && matchesType
  })
})

const showDeleteModal = ref(false)
const companyToDelete = ref<any>(null)
const isDeleting = ref(false)
const deleteError = ref<string | null>(null)

function confirmDelete(company: any) {
  companyToDelete.value = company
  showDeleteModal.value = true
  deleteError.value = null
}

async function handleDelete() {
  if (!companyToDelete.value) return

  isDeleting.value = true
  deleteError.value = null

  try {
    await useApiFetch(`/core/companies/${companyToDelete.value.id}`, {
      method: 'DELETE'
    })
    showDeleteModal.value = false
    companyToDelete.value = null
    refresh()
    toast.add({ title: 'Company deleted' })
  } catch (err: any) {
    deleteError.value = err.data?.detail || err.message || 'Failed to delete company'
  } finally {
    isDeleting.value = false
  }
}

function getCompanyActions(company: any) {
  const actions: any[][] = [
    [
      { label: 'Edit', icon: 'i-heroicons-pencil-square', to: `/companies/${company.id}/edit` }
    ]
  ]

  actions.push([
    { label: 'Delete', icon: 'i-heroicons-trash', color: 'error', onSelect: () => confirmDelete(company) }
  ])

  return actions
}

function getTypeBadge(company: any) {
  if (company.is_manufacturer && company.is_vendor) {
    return { label: 'Both', color: 'purple' as const }
  } else if (company.is_manufacturer) {
    return { label: 'Manufacturer', color: 'blue' as const }
  } else {
    return { label: 'Vendor', color: 'green' as const }
  }
}
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

    <UCard>
      <div class="flex flex-col md:flex-row gap-4 mb-6">
        <UInput v-model="searchQuery" icon="i-heroicons-magnifying-glass" placeholder="Search companies..."
          class="flex-1" />
        <USelect v-model="typeFilter" :items="[
          { label: 'All Types', value: 'all' },
          { label: 'Manufacturers', value: 'manufacturer' },
          { label: 'Vendors', value: 'vendor' }
        ]" value-key="value" class="w-48" />
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div v-for="company in filteredCompanies" :key="company.id"
          class="p-4 border border-gray-200 dark:border-gray-800 rounded-lg hover:border-primary-500 dark:hover:border-primary-400 transition-colors group">
          <div class="flex items-start justify-between">
            <NuxtLink :to="`/companies/${company.id}`" class="flex-1">
              <h3 class="font-semibold text-lg group-hover:text-primary-500">{{ company.name }}</h3>
            </NuxtLink>
            <UDropdown-menu :items="getCompanyActions(company)">
              <UButton variant="ghost" color="gray" icon="i-heroicons-ellipsis-vertical" size="sm" />
            </UDropdown-menu>
          </div>

          <div class="mt-2 flex items-center gap-2">
            <UBadge v-bind="getTypeBadge(company)" size="sm" />
          </div>

          <div v-if="company.website" class="mt-3 text-sm text-gray-500 dark:text-gray-400">
            <UIcon name="i-heroicons-globe-alt" class="w-4 h-4 inline mr-1" />
            <a :href="company.website" target="_blank" class="hover:text-primary-500 truncate">{{ company.website }}</a>
          </div>
        </div>
      </div>

      <div v-if="!companies" class="text-center py-12">
        <UIcon name="i-heroicons-arrow-path" class="w-8 h-8 animate-spin text-gray-400 mx-auto" />
      </div>

      <div v-else-if="filteredCompanies.length === 0" class="text-center py-12 text-gray-500">
        <UIcon name="i-heroicons-building-office" class="w-12 h-12 mx-auto mb-4 opacity-50" />
        <p class="mb-4">No companies found matching your criteria.</p>
        <UButton icon="i-heroicons-plus" label="Add First Company" color="primary" to="/companies/new" />
      </div>
    </UCard>

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
