<script setup lang="ts">
import type { ColumnDef } from '@tanstack/vue-table'

interface Props {
  items: any[]
}

defineProps<Props>()

const columns: ColumnDef<any>[] = [
  { id: 'designators', accessorKey: 'designators', header: 'Designators', enableSorting: false },
  { id: 'quantity', accessorKey: 'quantity', header: 'Qty' },
  { id: 'mpn', accessorKey: 'mpn', header: 'MPN' },
  { id: 'match', accessorKey: 'match', header: 'Matched Part' },
  { id: 'status', accessorKey: 'status', header: 'Status' },
  { id: 'actions', accessorKey: 'actions', header: '', enableSorting: false }
]

const cardFields = ['quantity', 'mpn', 'status']
</script>

<template>
  <DataListView
    model-key="inventory"
    :column-defs="columns"
    :card-fields="cardFields"
    :data="items"
    :can-create="false"
    :can-delete="false"
    :can-search="false"
    :can-paginate="false"
  >
    <template #designators-cell="{ row }">
      <span class="font-mono text-xs">{{ row.designators.join(', ') }}</span>
    </template>

    <template #match-cell="{ row }">
      <div v-if="row.matchedPart" class="flex flex-col">
        <span class="font-medium text-sm">{{ row.matchedPart.name }}</span>
        <span class="text-xs text-gray-500 font-mono">{{ row.matchedPart.mpn }}</span>
      </div>
      <UButton
        v-else
        label="Match Part"
        variant="soft"
        color="warning"
        size="xs"
        icon="i-heroicons-link"
      />
    </template>

    <template #status-cell="{ row }">
      <UBadge :color="row.matchedPart ? 'success' : 'error'" variant="subtle" size="xs">
        {{ row.matchedPart ? 'Matched' : 'Unmatched' }}
      </UBadge>
    </template>

    <template #actions-cell="{ row }">
      <div class="flex justify-end gap-1">
        <UDropdownMenu
          :items="[[{ label: 'Set Substitute', icon: 'i-heroicons-arrow-path' }, { label: 'Ignore Line', icon: 'i-heroicons-eye-slash' }]]"
        >
          <UButton variant="ghost" color="neutral" icon="i-heroicons-ellipsis-horizontal" />
        </UDropdownMenu>
      </div>
    </template>
  </DataListView>
</template>
