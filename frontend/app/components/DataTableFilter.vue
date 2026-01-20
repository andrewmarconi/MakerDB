<script setup lang="ts">
interface FilterConfig {
  key: string
  label: string
  type: 'select' | 'input' | 'date'
  options?: { label: string; value: any }[]
}

interface Props {
  filters: FilterConfig[]
  modelValue: Record<string, any>
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'update:modelValue': [value: Record<string, any>]
  'filter-change': [filters: Record<string, any>]
}>()

const localFilters = computed({
  get: () => props.modelValue,
  set: (value) => {
    emit('update:modelValue', value)
    emit('filter-change', value)
  }
})

function handleFilterChange(key: string, value: any) {
  const newValue = { ...localFilters.value, [key]: value }
  emit('update:modelValue', newValue)
  emit('filter-change', newValue)
}
</script>

<template>
  <div class="flex flex-wrap gap-4">
    <div v-for="filter in filters" :key="filter.key" class="flex-1 min-w-[200px]">
      <USelect
        v-if="filter.type === 'select' && filter.options"
        v-model="localFilters[filter.key]"
        :items="filter.options"
        :placeholder="filter.label"
        @update:model-value="(value) => handleFilterChange(filter.key, value)"
      />

      <UInput
        v-else-if="filter.type === 'input'"
        v-model="localFilters[filter.key]"
        :placeholder="filter.label"
        @update:model-value="(value) => handleFilterChange(filter.key, value)"
      />

      <UInput
        v-else-if="filter.type === 'date'"
        v-model="localFilters[filter.key]"
        type="date"
        :placeholder="filter.label"
        @update:model-value="(value) => handleFilterChange(filter.key, value)"
      />
    </div>
  </div>
</template>
