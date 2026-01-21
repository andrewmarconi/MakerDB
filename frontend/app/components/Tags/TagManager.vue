<script setup lang="ts">
const props = defineProps({
  modelValue: {
    type: Array as PropType<string[]>,
    default: () => []
  },
  suggestions: {
    type: Array as PropType<string[]>,
    default: () => []
  }
})

const emit = defineEmits(['update:modelValue'])

// Normalize tags to lowercase when updating
function handleUpdate(tags: string[]) {
  emit('update:modelValue', tags.map(t => t.trim().toLowerCase()))
}
</script>

<template>
  <div class="space-y-2">
    <UInputTags
      :model-value="modelValue"
      @update:model-value="handleUpdate"
      placeholder="Add tag..."
      size="sm"
      variant="outline"
    />
    <p v-if="modelValue.length === 0" class="text-sm text-muted">No tags added yet.</p>
  </div>
</template>
