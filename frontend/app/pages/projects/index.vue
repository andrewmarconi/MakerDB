<script setup lang="ts">
import type { ColumnDef } from '@tanstack/vue-table'

definePageMeta({
  title: 'Projects'
})

useSeoMeta({
  title: 'Projects',
  description: 'Manage your Bill of Materials and calculate production costs.'
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
  { accessorKey: 'revision', header: 'Revision' }
]

const cardFields = ['status', 'revision', 'updated_at']

const { data, pending, error } = await useAsyncData(
  'projects',
  (_nuxtApp, { signal }) => $fetch<Project[]>('/db/projects/', { signal }),
)

const isLoading = computed(() => {
  if (pending) return true;
  if (error) return true;
  return false;
})

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
    <template v-if="error">
      <UAlert 
        color="error"
        title="There was a problem loading data"
        :description="error.message"
        icon="i-lucide-terminal"
       />
    </template>
    <DataTable 
      :data="data as Project[]" 
      :columns="columns" 
      :card-fields="cardFields" 
      searchable
      clickable-column="name" 
      :default-sort="{ id: 'updated_at', desc: true }" 
      :loading="!isLoading"
       :on-row-click="(item) => ({ path: `/projects/${item.id}` })" />
  </div>
</template>
