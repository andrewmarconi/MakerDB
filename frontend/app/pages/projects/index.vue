<script setup lang="ts">
import type { ColumnDef } from '@tanstack/vue-table'

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

const cardFields = ['status', 'revision', 'updated_at']

const { data: projects, pending } = await useAsyncData('projects', () =>
  $fetch<Project[]>('/db/projects/')
)

const projectData = computed(() => projects.value ?? [])

const loading = computed(() => projectsPending.value)
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

    <DataTable v-if="projects" :data="projectData" :columns="columns" :card-fields="cardFields" searchable
      clickable-column="name" default-sort="{ id: 'updated_at', desc: true }" :loading="loading"
      :on-row-click="(project) => ({ path: `/projects/${project.id}` })" />
    <UCard v-else>
      <div class="flex items-center justify-center py-12">
        <UIcon name="i-heroicons-arrow-path" class="w-8 h-8 animate-spin text-primary-500" />
        <span class="ml-3">Loading projects...</span>
      </div>
    </UCard>
  </div>
</template>
