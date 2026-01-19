<script setup>
const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update:modelValue'])

const newTag = ref('')

const addTag = () => {
  if (newTag.value && !props.modelValue.includes(newTag.value)) {
    emit('update:modelValue', [...props.modelValue, newTag.value])
    newTag.value = ''
  }
}

const removeTag = (tag) => {
  emit('update:modelValue', props.modelValue.filter(t => t !== tag))
}
</script>

<template>
  <div class="space-y-2">
    <div class="flex flex-wrap gap-2">
      <UBadge
        v-for="tag in modelValue"
        :key="tag"
        variant="subtle"
        color="primary"
        size="sm"
        class="group pr-1"
      >
        {{ tag }}
        <button @click="removeTag(tag)" class="ml-1 hover:text-red-500 opacity-50 group-hover:opacity-100 transition-opacity">
          <UIcon name="i-heroicons-x-mark" class="w-3 h-3" />
        </button>
      </UBadge>
      
      <UInput
        v-model="newTag"
        placeholder="Add tag..."
        size="xs"
        class="w-24"
        variant="none"
        @keyup.enter="addTag"
      />
    </div>
  </div>
</template>
