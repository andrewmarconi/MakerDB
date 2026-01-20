<script setup lang="ts">
import type { ColumnDef } from '@tanstack/vue-table'

interface Props {
  items: any[]
}

defineProps<Props>()

const columns: ColumnDef<any>[] = [
  { id: 'designators', key: 'designators', label: 'Designators', enableSorting: false },
  { id: 'quantity', key: 'quantity', label: 'Qty' },
  { id: 'mpn', key: 'mpn', label: 'MPN' },
  { id: 'match', key: 'match', label: 'Matched Part' },
  { id: 'status', key: 'status', label: 'Status' },
  { id: 'actions', key: 'actions', label: '', enableSorting: false }
]

const cardFields = ['quantity', 'mpn', 'status']
</script>

<template>
  <DataTable :data="items" :columns="columns" :card-fields="cardFields">
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
        color="orange"
        size="xs"
        icon="i-heroicons-link"
      />
    </template>

    <template #status-cell="{ row }">
      <UBadge :color="row.matchedPart ? 'green' : 'red'" variant="subtle" size="xs">
        {{ row.matchedPart ? 'Matched' : 'Unmatched' }}
      </UBadge>
    </template>

    <template #actions-cell="{ row }">
      <div class="flex justify-end gap-1">
        <UDropdownMenu
          :items="[[{ label: 'Set Substitute', icon: 'i-heroicons-arrow-path' }, { label: 'Ignore Line', icon: 'i-heroicons-eye-slash' }]]"
        >
          <UButton variant="ghost" color="gray" icon="i-heroicons-ellipsis-horizontal" />
        </UDropdownMenu>
      </div>
    </template>
  </DataTable>
</template>
