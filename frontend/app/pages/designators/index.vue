<script setup lang="ts">
definePageMeta({
  title: 'Designators'
})

const router = useRouter()
const toast = useToast()

const { data: designators, refresh } = await useApiFetch('/parts/designators')

const searchQuery = ref('')
const showDeleteModal = ref(false)
const designatorToDelete = ref<any>(null)
const isDeleting = ref(false)
const deleteError = ref<string | null>(null)

const filteredDesignators = computed(() => {
  if (!designators.value) return []

  return (designators.value as any[]).filter((designator: any) => {
    return designator.code.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      designator.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  })
})

function confirmDelete(designator: any) {
  designatorToDelete.value = designator
  showDeleteModal.value = true
  deleteError.value = null
}

async function handleDelete() {
  if (!designatorToDelete.value) return

  isDeleting.value = true
  deleteError.value = null

  try {
    await useApiFetch(`/parts/designators/${designatorToDelete.value.id}`, {
      method: 'DELETE'
    })
    showDeleteModal.value = false
    designatorToDelete.value = null
    refresh()
    toast.add({ title: 'Designator deleted' })
  } catch (err: any) {
    deleteError.value = err.data?.detail || err.message || 'Failed to delete designator'
  } finally {
    isDeleting.value = false
  }
}
</script>

<template>
  <div class="space-y-6">
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold">Designators</h1>
        <p class="text-gray-500 dark:text-gray-400">Manage component designator prefixes (e.g., R for Resistor, C for Capacitor).</p>
      </div>
      <div class="flex items-center gap-2">
        <UButton icon="i-heroicons-plus" label="Add Designator" color="primary" to="/designators/new" />
      </div>
    </div>

    <UCard>
      <template #header>
        <UInput v-model="searchQuery" icon="i-heroicons-magnifying-glass" placeholder="Search designators..."
          class="max-w-md" />
      </template>

      <div v-if="!designators" class="text-center py-12">
        <UIcon name="i-heroicons-arrow-path" class="w-8 h-8 animate-spin text-gray-400 mx-auto" />
      </div>

      <div v-else-if="filteredDesignators.length > 0" class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="border-b border-gray-200 dark:border-gray-700">
              <th class="text-left py-3 px-4 font-medium">Code</th>
              <th class="text-left py-3 px-4 font-medium">Name</th>
              <th class="text-right py-3 px-4 font-medium">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="designator in filteredDesignators" :key="designator.id"
              class="border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800/50">
              <td class="py-3 px-4 font-mono font-medium">{{ designator.code }}</td>
              <td class="py-3 px-4">{{ designator.name }}</td>
              <td class="py-3 px-4 text-right">
                <div class="flex items-center justify-end gap-1">
                  <UButton icon="i-heroicons-trash" size="xs" variant="ghost" color="red"
                    @click="confirmDelete(designator)" />
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-else class="text-center py-12 text-gray-500">
        <UIcon name="i-heroicons-tag" class="w-12 h-12 mx-auto mb-4 opacity-50" />
        <p class="mb-4">No designators found.</p>
        <UButton icon="i-heroicons-plus" label="Add First Designator" color="primary" to="/designators/new" />
      </div>
    </UCard>

    <UModal v-model:open="showDeleteModal">
      <template #header>
        <h3 class="text-lg font-semibold">Delete Designator</h3>
      </template>

      <template #body>
        <p class="text-gray-600 dark:text-gray-400">
          Are you sure you want to delete <strong>{{ designatorToDelete?.code }}</strong> ({{ designatorToDelete?.name }})?
          This action cannot be undone.
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
