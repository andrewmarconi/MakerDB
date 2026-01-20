<script setup lang="ts">
definePageMeta({
  title: 'Projects'
})

interface Project {
  id: string
  name: string
  status: string
  revision: string
  updated_at: string
}

const columns: ColumnDef<Project>[] = [
  { accessorKey: 'name', header: 'Project Name' },
  { accessorKey: 'status', header: 'Status' },
  { accessorKey: 'revision', header: 'Revision' },
  { accessorKey: 'updated_at', header: 'Last Modified' }
]

const { data: projects } = await useAsyncData('projects', () =>
  $fetch<Project[]>('/db/projects/')
)

const projectData = computed(() => projects.value ?? [])
</script>

<template>
  <div class="space-y-6">
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold">Projects</h1>
        <p class="text-gray-500 dark:text-gray-400">Manage your Bill of Materials and calculate production costs.</p>
      </div>
      <div class="flex items-center gap-2">
        <UButton icon="i-heroicons-plus" label="New Project" color="primary" to="/projects/new" />
      </div>
    </div>

    <UCard v-if="projects">
      <template v-if="projectData.length > 0">
        <UTable :data="projectData" :columns="columns">
          <template #name-header="{ column }">
            <span class="font-semibold">{{ column.columnDef.header }}</span>
          </template>
          <template #name-cell="{ row }">
            <NuxtLink :to="`/projects/${row.original.id}`" class="font-medium text-primary-500 hover:underline">
              {{ row.original.name }}
            </NuxtLink>
          </template>

          <template #status-cell="{ row }">
            <UBadge :color="row.original.status === 'draft' ? 'gray' : row.original.status === 'active' ? 'green' : 'blue'" variant="subtle">
              {{ row.original.status }}
            </UBadge>
          </template>

          <template #updated_at-cell="{ row }">
            {{ new Date(row.original.updated_at).toLocaleDateString() }}
          </template>
        </UTable>
      </template>

      <template v-else>
        <div class="flex flex-col items-center justify-center py-12 text-gray-400">
          <UIcon name="i-heroicons-folder-open" class="w-12 h-12 mb-4 opacity-50" />
          <p class="mb-4">No projects yet. Create your first project to get started.</p>
          <UButton icon="i-heroicons-plus" label="Create Project" color="primary" to="/projects/new" />
        </div>
      </template>
    </UCard>

    <UCard v-else>
      <div class="flex items-center justify-center py-12">
        <UIcon name="i-heroicons-arrow-path" class="w-8 h-8 animate-spin text-primary-500" />
        <span class="ml-3">Loading projects...</span>
      </div>
    </UCard>
  </div>
</template>
