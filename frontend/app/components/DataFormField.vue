<script setup lang="ts">
import type { tFieldSchema, tFieldState } from '~/shared/types/ui'
import TagManager from '~/components/Tags/TagManager.vue'

const props = defineProps<{
  schema: tFieldSchema
  modelValue: any
  state: tFieldState
  error?: string | null
  readonly?: boolean
}>()

const emit = defineEmits<{
  'update:modelValue': [value: any]
  'focus': []
  'blur': []
  'save': []
  'cancel': []
}>()

const inputRef = ref<HTMLInputElement | null>(null)
const localValue = ref(props.modelValue)

// Sync local value when modelValue changes externally
watch(() => props.modelValue, (newVal) => {
  if (props.state !== 'editing') {
    localValue.value = newVal
  }
})

// Focus input when entering edit mode
watch(() => props.state, (newState) => {
  if (newState === 'editing') {
    nextTick(() => {
      const inputEl = inputRef.value?.$el?.querySelector?.('input, textarea, select')
      inputEl?.focus?.()
    })
  }
})

const isEditing = computed(() => props.state === 'editing')
const isSaving = computed(() => props.state === 'saving')
const isSuccess = computed(() => props.state === 'success')
const isError = computed(() => props.state === 'error')
const canEdit = computed(() => !props.readonly && !props.schema.readonly)

function handleClick() {
  if (canEdit.value && props.state === 'idle') {
    localValue.value = props.modelValue
    emit('focus')
  }
}

function handleBlur() {
  if (isEditing.value) {
    emit('update:modelValue', localValue.value)
    emit('blur')
  }
}

function handleKeydown(e: KeyboardEvent) {
  if (e.key === 'Escape') {
    localValue.value = props.modelValue
    emit('cancel')
  } else if (e.key === 'Enter' && props.schema.type !== 'textarea') {
    emit('update:modelValue', localValue.value)
    emit('save')
  }
}

function handleTagsUpdate(tags: string[]) {
  localValue.value = tags
  emit('update:modelValue', tags)
  emit('blur')
}

// Format display value for read-only mode
const displayValue = computed(() => {
  const val = props.modelValue
  if (val === null || val === undefined || val === '') {
    return '—'
  }
  if (props.schema.type === 'checkbox') {
    return val ? 'Yes' : 'No'
  }
  if (props.schema.type === 'select' && props.schema.options) {
    const option = props.schema.options.find(o => o.value === val)
    return option?.label ?? val
  }
  if (props.schema.type === 'tags' && Array.isArray(val)) {
    return val.length > 0 ? val : '—'
  }
  return val
})
</script>

<template>
  <div
    class="group relative"
    :class="[
      schema.span === 2 ? 'col-span-2' : '',
      canEdit && state === 'idle' ? 'cursor-pointer' : ''
    ]"
  >
    <!-- Label -->
    <label class="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
      {{ schema.label }}
      <span v-if="schema.required" class="text-red-500">*</span>
    </label>

    <!-- Read-only display -->
    <div
      v-if="!isEditing && schema.type !== 'tags'"
      class="relative min-h-[2.5rem] flex items-center rounded-md px-3 py-2 transition-all duration-150"
      :class="[
        canEdit && state === 'idle' ? 'hover:bg-gray-50 dark:hover:bg-gray-800 hover:ring-1 hover:ring-gray-200 dark:hover:ring-gray-700' : '',
        isSaving ? 'bg-gray-50 dark:bg-gray-800' : '',
        isSuccess ? 'bg-green-50 dark:bg-green-900/20 ring-1 ring-green-200 dark:ring-green-800' : '',
        isError ? 'bg-red-50 dark:bg-red-900/20 ring-1 ring-red-200 dark:ring-red-800' : ''
      ]"
      @click="handleClick"
    >
      <!-- Display value -->
      <span
        class="text-gray-900 dark:text-gray-100"
        :class="[
          displayValue === '—' ? 'text-gray-400 dark:text-gray-500 italic' : ''
        ]"
      >
        {{ displayValue }}
      </span>

      <!-- Edit hint icon (on hover) -->
      <UIcon
        v-if="canEdit && state === 'idle'"
        name="i-heroicons-pencil"
        class="absolute right-2 w-4 h-4 text-gray-400 opacity-0 group-hover:opacity-100 transition-opacity"
      />

      <!-- Saving spinner -->
      <UIcon
        v-if="isSaving"
        name="i-heroicons-arrow-path"
        class="absolute right-2 w-4 h-4 text-gray-400 animate-spin"
      />

      <!-- Success checkmark -->
      <UIcon
        v-if="isSuccess"
        name="i-heroicons-check-circle"
        class="absolute right-2 w-4 h-4 text-green-500"
      />

      <!-- Error icon -->
      <UIcon
        v-if="isError"
        name="i-heroicons-exclamation-circle"
        class="absolute right-2 w-4 h-4 text-red-500"
      />
    </div>

    <!-- Tags field (special handling - always visible) -->
    <div
      v-else-if="schema.type === 'tags'"
      class="relative min-h-[2.5rem] rounded-md transition-all duration-150"
      :class="[
        isSaving ? 'opacity-50 pointer-events-none' : '',
        isSuccess ? 'ring-1 ring-green-200 dark:ring-green-800' : '',
        isError ? 'ring-1 ring-red-200 dark:ring-red-800' : ''
      ]"
    >
      <TagManager
        :model-value="(localValue as string[]) || []"
        :readonly="!canEdit"
        @update:model-value="handleTagsUpdate"
      />
    </div>

    <!-- Edit mode inputs -->
    <template v-else-if="isEditing">
      <!-- Text input -->
      <UInput
        v-if="schema.type === 'text'"
        ref="inputRef"
        v-model="localValue"
        :placeholder="schema.placeholder"
        class="w-full"
        @blur="handleBlur"
        @keydown="handleKeydown"
      />

      <!-- Textarea -->
      <UTextarea
        v-else-if="schema.type === 'textarea'"
        ref="inputRef"
        v-model="localValue"
        :placeholder="schema.placeholder"
        :rows="3"
        class="w-full"
        @blur="handleBlur"
        @keydown="handleKeydown"
      />

      <!-- Number input -->
      <UInput
        v-else-if="schema.type === 'number'"
        ref="inputRef"
        v-model.number="localValue"
        type="number"
        :placeholder="schema.placeholder"
        class="w-full"
        @blur="handleBlur"
        @keydown="handleKeydown"
      />

      <!-- Select -->
      <USelect
        v-else-if="schema.type === 'select'"
        ref="inputRef"
        v-model="localValue"
        :items="schema.options || []"
        value-key="value"
        :placeholder="schema.placeholder || 'Select...'"
        class="w-full"
        @blur="handleBlur"
        @update:model-value="handleBlur"
      />

      <!-- Checkbox -->
      <div v-else-if="schema.type === 'checkbox'" class="py-2">
        <UCheckbox
          v-model="localValue"
          :label="localValue ? 'Yes' : 'No'"
          @update:model-value="handleBlur"
        />
      </div>

      <!-- Custom component -->
      <component
        v-else-if="schema.type === 'custom' && schema.component"
        :is="schema.component"
        v-model="localValue"
        v-bind="schema.componentProps"
        @blur="handleBlur"
      />
    </template>

    <!-- Error message -->
    <p v-if="error" class="mt-1 text-sm text-red-500">
      {{ error }}
    </p>
  </div>
</template>
