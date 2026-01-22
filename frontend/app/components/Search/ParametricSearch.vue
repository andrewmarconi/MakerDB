<script setup lang="ts">
import { parseUnit } from '~/utils/unit-parser'

const props = defineProps({
  label: String
})

const emit = defineEmits(['filter'])

const rawValue = ref('')
const value = computed(() => parseUnit(rawValue.value))

watch(value, (newVal) => {
  emit('filter', newVal)
})
</script>

<template>
  <UFormField :label="label">
    <UInput
      v-model="rawValue"
      placeholder="e.g. 10k, 1uF, 4.7M"
      icon="i-heroicons-adjustments-horizontal"
    >
      <template #trailing>
        <div v-if="value !== null" class="text-xs text-gray-500 bg-gray-100 dark:bg-gray-800 px-1.5 py-0.5 rounded border border-gray-200 dark:border-gray-700">
          = {{ value }}
        </div>
      </template>
    </UInput>
  </UFormField>
</template>
