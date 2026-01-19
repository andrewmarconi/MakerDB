<script setup>
const props = defineProps({
  items: {
    type: Array,
    required: true
  }
})

const columns = [
  { id: 'designators', key: 'designators', label: 'Designators' },
  { id: 'quantity', key: 'quantity', label: 'Qty' },
  { id: 'mpn', key: 'mpn', label: 'MPN' },
  { id: 'match', key: 'match', label: 'Matched Part' },
  { id: 'status', key: 'status', label: 'Status' },
  { id: 'actions', key: 'actions', label: '' }
]
</script>

<template>
  <div class="space-y-4">
    <UTable :columns="columns" :rows="items">
      <template #designators-data="{ row }">
        <span class="font-mono text-xs">{{ row.designators.join(', ') }}</span>
      </template>

      <template #match-data="{ row }">
        <div v-if="row.matchedPart" class="flex flex-col">
          <span class="font-medium text-sm">{{ row.matchedPart.name }}</span>
          <span class="text-xs text-gray-500 font-mono">{{ row.matchedPart.mpn }}</span>
        </div>
        <UButton v-else label="Match Part" variant="soft" color="orange" size="xs" icon="i-heroicons-link" />
      </template>

      <template #status-data="{ row }">
        <UBadge :color="row.matchedPart ? 'green' : 'red'" variant="subtle" size="xs">
          {{ row.matchedPart ? 'Matched' : 'Unmatched' }}
        </UBadge>
      </template>

      <template #actions-data="{ row }">
        <UDropdownMenu
          :items="[[{ label: 'Set Substitute', icon: 'i-heroicons-arrow-path' }, { label: 'Ignore Line', icon: 'i-heroicons-eye-slash' }]]">
          <UButton variant="ghost" color="gray" icon="i-heroicons-ellipsis-horizontal" />
        </UDropdownMenu>
      </template>
    </UTable>
  </div>
</template>
