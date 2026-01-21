<script setup lang="ts">
import type { FieldSchema, FieldState } from '~/shared/types/ui'
import DataFormField from '~/components/DataFormField.vue'

const props = withDefaults(defineProps<{
  modelValue: Record<string, any>
  schema: FieldSchema[]
  endpoint: string
  entityId: string
  saveMode?: 'patch' | 'put'
  debounceMs?: number
  layout?: 'single' | 'two-column'
  readonly?: boolean
}>(), {
  saveMode: 'patch',
  debounceMs: 500,
  layout: 'single',
  readonly: false
})

const emit = defineEmits<{
  'update:modelValue': [value: Record<string, any>]
  'save': [field: string, value: any, response: any]
  'save-error': [field: string, error: Error]
  'field-focus': [field: string]
  'field-blur': [field: string]
}>()

// Track state for each field
const fieldStates = ref<Record<string, FieldState>>({})
const fieldErrors = ref<Record<string, string | null>>({})
const originalValues = ref<Record<string, any>>({})
const pendingSaves = ref<Record<string, ReturnType<typeof setTimeout>>>({})

// Initialize field states
onMounted(() => {
  props.schema.forEach(field => {
    fieldStates.value[field.key] = 'idle'
    fieldErrors.value[field.key] = null
    originalValues.value[field.key] = props.modelValue[field.key]
  })
})

// Watch for external modelValue changes
watch(() => props.modelValue, (newVal) => {
  props.schema.forEach(field => {
    if (fieldStates.value[field.key] === 'idle') {
      originalValues.value[field.key] = newVal[field.key]
    }
  })
}, { deep: true })

function getFieldState(key: string): FieldState {
  return fieldStates.value[key] || 'idle'
}

function getFieldError(key: string): string | null {
  return fieldErrors.value[key] || null
}

function handleFieldFocus(field: FieldSchema) {
  fieldStates.value[field.key] = 'editing'
  fieldErrors.value[field.key] = null
  originalValues.value[field.key] = props.modelValue[field.key]
  emit('field-focus', field.key)
}

function handleFieldBlur(field: FieldSchema) {
  emit('field-blur', field.key)

  // Check if value actually changed
  const currentValue = props.modelValue[field.key]
  const originalValue = originalValues.value[field.key]

  if (JSON.stringify(currentValue) === JSON.stringify(originalValue)) {
    fieldStates.value[field.key] = 'idle'
    return
  }

  // Validate before saving
  if (field.validator) {
    const error = field.validator(currentValue)
    if (error) {
      fieldErrors.value[field.key] = error
      fieldStates.value[field.key] = 'error'
      return
    }
  }

  // Required field validation
  if (field.required && (currentValue === null || currentValue === undefined || currentValue === '')) {
    fieldErrors.value[field.key] = `${field.label} is required`
    fieldStates.value[field.key] = 'error'
    return
  }

  // Clear any existing pending save for this field
  if (pendingSaves.value[field.key]) {
    clearTimeout(pendingSaves.value[field.key])
  }

  // Debounce the save
  pendingSaves.value[field.key] = setTimeout(() => {
    saveField(field)
  }, props.debounceMs)
}

function handleFieldUpdate(field: FieldSchema, value: any) {
  const newModelValue = { ...props.modelValue, [field.key]: value }
  emit('update:modelValue', newModelValue)
}

function handleFieldSave(field: FieldSchema) {
  // Clear debounce and save immediately
  if (pendingSaves.value[field.key]) {
    clearTimeout(pendingSaves.value[field.key])
  }
  saveField(field)
}

function handleFieldCancel(field: FieldSchema) {
  // Clear any pending save
  if (pendingSaves.value[field.key]) {
    clearTimeout(pendingSaves.value[field.key])
  }

  // Revert to original value
  const newModelValue = { ...props.modelValue, [field.key]: originalValues.value[field.key] }
  emit('update:modelValue', newModelValue)

  fieldStates.value[field.key] = 'idle'
  fieldErrors.value[field.key] = null
}

async function saveField(field: FieldSchema) {
  const value = props.modelValue[field.key]

  fieldStates.value[field.key] = 'saving'
  fieldErrors.value[field.key] = null

  try {
    let response: any

    if (props.saveMode === 'patch') {
      // PATCH - send only the changed field
      response = await $fetch(`/db${props.endpoint}/${props.entityId}`, {
        method: 'PATCH',
        body: { [field.key]: value }
      })
    } else {
      // PUT - send full object
      response = await $fetch(`/db${props.endpoint}/${props.entityId}`, {
        method: 'PUT',
        body: props.modelValue
      })
    }

    // Success!
    fieldStates.value[field.key] = 'success'
    originalValues.value[field.key] = value
    emit('save', field.key, value, response)

    // Reset to idle after success animation
    setTimeout(() => {
      if (fieldStates.value[field.key] === 'success') {
        fieldStates.value[field.key] = 'idle'
      }
    }, 1500)

  } catch (err: any) {
    // Error - revert and show error
    fieldStates.value[field.key] = 'error'
    fieldErrors.value[field.key] = err.data?.detail || err.message || 'Failed to save'

    // Revert to original value
    const newModelValue = { ...props.modelValue, [field.key]: originalValues.value[field.key] }
    emit('update:modelValue', newModelValue)
    emit('save-error', field.key, err)

    // Reset to idle after error display
    setTimeout(() => {
      if (fieldStates.value[field.key] === 'error') {
        fieldStates.value[field.key] = 'idle'
        fieldErrors.value[field.key] = null
      }
    }, 3000)
  }
}

// Clean up pending saves on unmount
onUnmounted(() => {
  Object.values(pendingSaves.value).forEach(timeout => {
    clearTimeout(timeout)
  })
})
</script>

<template>
  <div
    class="space-y-4"
    :class="[
      layout === 'two-column' ? 'grid grid-cols-1 md:grid-cols-2 gap-4' : ''
    ]"
  >
    <DataFormField
      v-for="field in schema"
      :key="field.key"
      :schema="field"
      :model-value="modelValue[field.key]"
      :state="getFieldState(field.key)"
      :error="getFieldError(field.key)"
      :readonly="readonly"
      @update:model-value="(val) => handleFieldUpdate(field, val)"
      @focus="handleFieldFocus(field)"
      @blur="handleFieldBlur(field)"
      @save="handleFieldSave(field)"
      @cancel="handleFieldCancel(field)"
    />
  </div>
</template>
