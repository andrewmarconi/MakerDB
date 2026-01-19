<script setup>
const columns = [
  { id: 'name', key: 'name', label: 'Project Name', sortable: true },
  { id: 'status', key: 'status', label: 'Status' },
  { id: 'bomItems', key: 'bomItems', label: 'BOM Items' },
  { id: 'valuation', key: 'valuation', label: 'Valuation', sortable: true },
  { id: 'lastModified', key: 'lastModified', label: 'Last Modified', sortable: true },
  { id: 'actions', key: 'actions', label: '' }
]

const { data: projects, refresh } = await useApiFetch('/projects/')

</script>

<template>
  <div class="space-y-6">
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold">Projects</h1>
        <p class="text-gray-500 dark:text-gray-400">Manage your Bill of Materials and calculate production costs.</p>
      </div>
      <div class="flex items-center gap-2">
        <UButton icon="i-heroicons-plus" label="New Project" color="primary" />
      </div>
    </div>

    <UCard>
      <UTable :columns="columns" :rows="projects">
        <template #status-data="{ row }">
          <StatusBadge :status="row.status" />
        </template>

        <template #actions-data="{ row }">
          <div class="flex justify-end">
            <UButton variant="ghost" color="gray" icon="i-heroicons-eye" :to="`/projects/${row.id}`" />
          </div>
        </template>
      </UTable>
    </UCard>
  </div>
</template>
