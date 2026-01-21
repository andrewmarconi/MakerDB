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

const newTag = ref('')
const isDropdownOpen = ref(false)

const allSuggestions = computed(() => {
  const baseSuggestions = [
    'capacitor', 'resistor', 'connector', 'ic', 'microcontroller', 'sensor',
    'led', 'display', 'battery', 'connector', 'wire', 'switch', 'relay',
    'transformer', 'inductor', 'crystal', 'oscillator', 'fuse', 'connector',
    'pcb', 'enclosure', 'fastener', 'screw', 'nut', 'washer', 'adhesive',
    'through-hole', 'smd', 'bga', 'qfp', 'sop', 'dip', 'soic', 'tqfp',
    '3.3v', '5v', '12v', '24v', 'analog', 'digital', 'power', 'signal'
  ]
  const extra = props.suggestions || []
  return [...new Set([...baseSuggestions, ...extra])]
})

const filteredSuggestions = computed(() => {
  if (!newTag.value.trim()) return allSuggestions.value.filter(s => !props.modelValue.includes(s))
  return allSuggestions.value.filter(s =>
    s.toLowerCase().includes(newTag.value.toLowerCase().trim()) &&
    !props.modelValue.includes(s)
  ).slice(0, 10)
})

function addTag(tag?: string) {
  const tagToAdd = (tag || newTag.value).trim().toLowerCase()
  if (tagToAdd && !props.modelValue.includes(tagToAdd)) {
    emit('update:modelValue', [...props.modelValue, tagToAdd])
  }
  newTag.value = ''
  isDropdownOpen.value = false
}

function removeTag(tag: string) {
  emit('update:modelValue', props.modelValue.filter(t => t !== tag))
}

function handleKeydown(e: KeyboardEvent) {
  if (e.key === 'Enter' || e.key === ',') {
    e.preventDefault()
    addTag()
  } else if (e.key === 'Backspace' && !newTag.value && props.modelValue.length > 0) {
    const lastTag = props.modelValue[props.modelValue.length - 1]
    if (lastTag !== undefined) {
      removeTag(lastTag)
    }
  } else if (e.key === 'Escape') {
    isDropdownOpen.value = false
  }
}

function handleBlur() {
  setTimeout(() => {
    isDropdownOpen.value = false
  }, 200)
}

function handleFocus() {
  if (newTag.value || filteredSuggestions.value.length > 0) {
    isDropdownOpen.value = true
  }
}
</script>

<template>
  <div class="space-y-2">
    <div class="flex flex-wrap gap-2">
      <UBadge v-for="tag in modelValue" :key="tag" variant="subtle" color="primary" size="sm"
        class="group pr-1 cursor-default">
        {{ tag }}
        <button @click="removeTag(tag)"
          class="ml-1 hover:text-red-500 opacity-50 group-hover:opacity-100 transition-opacity" tabindex="-1">
          <UIcon name="i-heroicons-x-mark" class="w-3 h-3" />
        </button>
      </UBadge>

      <div class="relative">
        <UInput v-model="newTag" placeholder="Add tag..." size="xs" class="w-32" variant="outline"
          @keydown="handleKeydown" @focus="handleFocus" @blur="handleBlur" @input="isDropdownOpen = true" />

        <UCommandMenu v-model="isDropdownOpen" :items="filteredSuggestions.map(s => ({ label: s, value: s }))"
          :popper="{ placement: 'bottom-start' }" @update:modelValue="addTag($event?.value)">
          <template #item="{ item }">
            <span>{{ item.label }}</span>
          </template>
        </UCommandMenu>
      </div>
    </div>

    <p v-if="modelValue.length === 0" class="text-sm text-gray-500">No tags added yet.</p>
  </div>
</template>
