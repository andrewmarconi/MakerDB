<script setup lang="ts">
import type { ColumnDef } from '@tanstack/vue-table'

definePageMeta({
  title: 'Projects'
})

useSeoMeta({
  title: 'Projects',
  description: 'Manage your Bill of Materials and calculate production costs.'
})

const columns: ColumnDef<Project>[] = [
  { accessorKey: 'name', header: 'Project Name' },
  { accessorKey: 'status', header: 'Status' },
  { accessorKey: 'revision', header: 'Revision' }
]

const cardFields = ['status', 'revision', 'updated_at']
</script>

<template>
  <DataListView
    model-key="projects"
    :column-defs="columns"
    :card-fields="cardFields"
    :default-sort="{ id: 'updated_at', desc: true }"
  />
</template>
