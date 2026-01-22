<script setup lang="ts" generic="T extends Record<string, any>">
import type { tFieldSchema, tFieldState } from '~/shared/types/ui'
import DataFormField from '~/components/DataFormField.vue'

interface DisplayColumn {
  key: string
  label: string
  render?: (item: T) => any
}

const props = withDefaults(defineProps<{
  items: T[]
  itemSchema: tFieldSchema[]
  displayColumns?: DisplayColumn[]
  baseEndpoint: string
  title?: string
  addButtonLabel?: string
  emptyStateMessage?: string
  canEdit?: boolean
  canDelete?: boolean
  loading?: boolean
}>(), {
  displayColumns: () => [],
  addButtonLabel: 'Add Item',
  emptyStateMessage: 'No items yet.',
  canEdit: true,
  canDelete: true,
  loading: false,
  title: ''
})

const emit = defineEmits<{
  'item-added': [item: T]
  'item-updated': [item: T, changes: Record<string, any>]
  'item-deleted': [id: string]
  'refresh': []
}>()

const toast = useToast()

const editingRows = ref<Record<string, Record<string, tFieldState>>>({})
const editingValues = ref<Record<string, Record<string, any>>>({})
const pendingSaves = ref<Record<string, Record<string, ReturnType<typeof setTimeout>>>>({})
const fieldErrors = ref<Record<string, Record<string, string | null>>>({})

const showAddForm = ref(false)
const isAdding = ref(false)
const newItemForm = ref<Record<string, any>>({})
const newItemErrors = ref<Record<string, string | null>>({})

const searchState = ref<Record<string, { query: string; results: any[]; loading: boolean }>>({})
let searchTimeout: ReturnType<typeof setTimeout> | null = null

const isInitialized = ref(false)

onMounted(() => {
  props.items.forEach(item => {
    initializeRow(item.id)
  })
  isInitialized.value = true
})

function initializeRow(itemId: string) {
  if (!editingRows.value[itemId]) {
    editingRows.value[itemId] = {}
    editingValues.value[itemId] = {}
    fieldErrors.value[itemId] = {}
    props.itemSchema.forEach(field => {
      editingRows.value[itemId][field.key] = 'idle'
      fieldErrors.value[itemId][field.key] = null
    })
  }
}

watch(() => props.items, (newItems) => {
  if (!isInitialized.value) return
  newItems.forEach(item => {
    if (!editingRows.value[item.id]) {
      initializeRow(item.id)
    }
  })
}, { deep: true })

function getRowState(itemId: string, fieldKey: string): tFieldState {
  return editingRows.value[itemId]?.[fieldKey] || 'idle'
}

function getRowError(itemId: string, fieldKey: string): string | null {
  return fieldErrors.value[itemId]?.[fieldKey] || null
}

function handleFieldFocus(itemId: string, field: tFieldSchema) {
  if (!editingValues.value[itemId]) {
    editingValues.value[itemId] = { ...props.items.find(i => i.id === itemId) }
  }
  editingRows.value[itemId][field.key] = 'editing'
  fieldErrors.value[itemId][field.key] = null
}

function handleFieldBlur(itemId: string, field: tFieldSchema) {
  const currentValue = editingValues.value[itemId]?.[field.key]
  const originalValue = props.items.find(i => i.id === itemId)?.[field.key]

  if (JSON.stringify(currentValue) === JSON.stringify(originalValue)) {
    editingRows.value[itemId][field.key] = 'idle'
    return
  }

  if (field.validator) {
    const error = field.validator(currentValue)
    if (error) {
      fieldErrors.value[itemId][field.key] = error
      editingRows.value[itemId][field.key] = 'error'
      return
    }
  }

  if (field.required && (currentValue === null || currentValue === undefined || currentValue === '')) {
    fieldErrors.value[itemId][field.key] = `${field.label} is required`
    editingRows.value[itemId][field.key] = 'error'
    return
  }

  if (pendingSaves.value[itemId]?.[field.key]) {
    clearTimeout(pendingSaves.value[itemId][field.key])
  }

  pendingSaves.value[itemId] = pendingSaves.value[itemId] || {}
  pendingSaves.value[itemId][field.key] = setTimeout(() => {
    saveField(itemId, field)
  }, 500)
}

function handleFieldUpdate(itemId: string, field: tFieldSchema, value: any) {
  editingValues.value[itemId] = { ...editingValues.value[itemId], [field.key]: value }
}

async function saveField(itemId: string, field: tFieldSchema) {
  const value = editingValues.value[itemId]?.[field.key]
  editingRows.value[itemId][field.key] = 'saving'
  fieldErrors.value[itemId][field.key] = null

  try {
    const response = await $fetch<T>(`/db${props.baseEndpoint}/${itemId}`, {
      method: 'PATCH',
      body: { [field.key]: value }
    })

    editingRows.value[itemId][field.key] = 'success'
    emit('item-updated', response, { [field.key]: value })

    setTimeout(() => {
      if (editingRows.value[itemId]?.[field.key] === 'success') {
        editingRows.value[itemId][field.key] = 'idle'
      }
    }, 1500)
  } catch (err: any) {
    editingRows.value[itemId][field.key] = 'error'
    fieldErrors.value[itemId][field.key] = err.data?.detail || err.message || 'Failed to save'
    setTimeout(() => {
      if (editingRows.value[itemId]?.[field.key] === 'error') {
        editingRows.value[itemId][field.key] = 'idle'
        fieldErrors.value[itemId][field.key] = null
      }
    }, 3000)
  }
}

async function handleDelete(item: T) {
  if (!confirm(`Delete this item?`)) return

  try {
    await $fetch(`/db${props.baseEndpoint}/${item.id}`, { method: 'DELETE' })
    toast.add({ title: 'Item deleted', icon: 'i-heroicons-check-circle' })
    emit('item-deleted', item.id)
    emit('refresh')
  } catch (err: any) {
    toast.add({ title: 'Failed to delete', description: err.data?.detail || err.message, color: 'error' })
  }
}

function initNewItemForm() {
  const form: Record<string, any> = {}
  props.itemSchema.forEach(field => {
    form[field.key] = field.type === 'number' ? 0 : ''
  })
  newItemForm.value = form
  newItemErrors.value = {}
  showAddForm.value = true
  nextTick(() => {
    const firstField = props.itemSchema[0]
    if (firstField) {
      editingValues.value['__new__'] = { ...form }
      initializeRow('__new__')
    }
  })
}

function cancelAdd() {
  showAddForm.value = false
  newItemForm.value = {}
  editingRows.value['__new__'] = {}
  editingValues.value['__new__'] = {}
  searchState.value = {}
}

async function handleSearch(field: tFieldSchema, query: string) {
  if (!field.searchEndpoint) return

  searchState.value[field.key] = {
    query,
    results: [],
    loading: true
  }

  if (searchTimeout) clearTimeout(searchTimeout)

  if (!query.trim()) {
    searchState.value[field.key].results = []
    searchState.value[field.key].loading = false
    return
  }

  searchTimeout = setTimeout(async () => {
    try {
      const queryParam = field.searchQueryParam || 'search'
      const results = await $fetch<any[]>(`/db${field.searchEndpoint}?${queryParam}=${encodeURIComponent(query)}`)
      const valueKey = field.searchValueKey || 'id'
      const labelKey = field.searchLabelKey || 'name'
      searchState.value[field.key].results = results.map(r => ({
        value: r[valueKey],
        label: r[labelKey],
        data: r
      }))
    } catch (err) {
      searchState.value[field.key].results = []
    } finally {
      searchState.value[field.key].loading = false
    }
  }, 300)
}

function selectSearchResult(field: tFieldSchema, result: any) {
  newItemForm.value[field.key] = result.value
  newItemForm.value[`${field.key}_data`] = result.data
  searchState.value[field.key].results = []
  searchState.value[field.key].query = result.label
}

async function handleAddItem() {
  for (const field of props.itemSchema) {
    if (field.required && !newItemForm.value[field.key]) {
      newItemErrors.value[field.key] = `${field.label} is required`
      return
    }
    if (field.validator) {
      const error = field.validator(newItemForm.value[field.key])
      if (error) {
        newItemErrors.value[field.key] = error
        return
      }
    }
  }

  isAdding.value = true
  try {
    const response = await $fetch<T>(`/db${props.baseEndpoint}`, {
      method: 'POST',
      body: newItemForm.value
    })
    toast.add({ title: 'Item added', icon: 'i-heroicons-check-circle' })
    emit('item-added', response)
    emit('refresh')
    cancelAdd()
  } catch (err: any) {
    toast.add({ title: 'Failed to add item', description: err.data?.detail || err.message, color: 'error' })
  } finally {
    isAdding.value = false
  }
}

onUnmounted(() => {
  Object.values(pendingSaves.value).forEach(row => {
    Object.values(row).forEach(timeout => clearTimeout(timeout))
  })
})

defineExpose({
  initNewItemForm
})
</script>

<template>
  <div class="space-y-4">
    <UCard>
      <template #header v-if="title">
        <h3 class="font-semibold">{{ title }}</h3>
      </template>

      <div v-if="loading" class="flex items-center justify-center py-12">
        <UIcon name="i-heroicons-arrow-path" class="w-6 h-6 animate-spin text-gray-400" />
      </div>

      <div v-else-if="items.length === 0 && !showAddForm" class="flex flex-col items-center justify-center py-12 text-gray-400">
        <UIcon name="i-heroicons-inbox" class="w-12 h-12 mb-2 opacity-50" />
        <p>{{ emptyStateMessage }}</p>
      </div>

      <div v-else class="space-y-4">
        <div v-if="showAddForm" class="border-2 border-dashed border-primary-200 dark:border-primary-800 rounded-lg p-4 bg-primary-50 dark:bg-primary-900/20">
          <div class="flex items-center justify-between mb-3">
            <h4 class="font-medium text-primary-700 dark:text-primary-300">Add New Item</h4>
            <UButton icon="i-heroicons-x-mark" size="xs" color="gray" variant="ghost" @click="cancelAdd" />
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div v-for="field in itemSchema" :key="field.key" class="space-y-1">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                {{ field.label }}
                <span v-if="field.required" class="text-red-500">*</span>
              </label>
              <UInput
                v-if="field.type === 'text'"
                v-model="newItemForm[field.key]"
                :placeholder="field.placeholder"
                :color="newItemErrors[field.key] ? 'red' : 'gray'"
              />
              <UInput
                v-else-if="field.type === 'number'"
                v-model.number="newItemForm[field.key]"
                type="number"
                :placeholder="field.placeholder"
                :color="newItemErrors[field.key] ? 'red' : 'gray'"
              />
              <UTextarea
                v-else-if="field.type === 'textarea'"
                v-model="newItemForm[field.key]"
                :placeholder="field.placeholder"
                :rows="2"
                :color="newItemErrors[field.key] ? 'red' : 'gray'"
              />
              <USelect
                v-else-if="field.type === 'select'"
                v-model="newItemForm[field.key]"
                :items="field.options || []"
                value-key="value"
                :placeholder="field.placeholder || 'Select...'"
              />
              <div v-else-if="field.type === 'search'" class="relative">
                <UInput
                  v-model="newItemForm[field.key]"
                  :placeholder="field.placeholder || 'Search...'"
                  :color="newItemErrors[field.key] ? 'red' : 'gray'"
                  @input="handleSearch(field, ($event.target as HTMLInputElement).value)"
                />
                <div
                  v-if="searchState[field.key]?.results?.length > 0"
                  class="absolute z-10 w-full mt-1 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg max-h-48 overflow-y-auto"
                >
                  <button
                    v-for="result in searchState[field.key].results"
                    :key="result.value"
                    class="w-full px-3 py-2 text-left hover:bg-gray-100 dark:hover:bg-gray-700 text-sm"
                    @click="selectSearchResult(field, result)"
                  >
                    {{ result.label }}
                  </button>
                </div>
                <div v-if="searchState[field.key]?.loading" class="absolute right-3 top-2.5">
                  <UIcon name="i-heroicons-arrow-path" class="w-4 h-4 animate-spin text-gray-400" />
                </div>
              </div>
              <p v-if="newItemErrors[field.key]" class="text-sm text-red-500">{{ newItemErrors[field.key] }}</p>
            </div>
          </div>
          <div class="flex justify-end gap-2 mt-4">
            <UButton variant="ghost" color="gray" label="Cancel" @click="cancelAdd" />
            <UButton label="Add Item" icon="i-heroicons-plus" :loading="isAdding" @click="handleAddItem" />
          </div>
        </div>

        <div v-if="items.length > 0" class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead>
              <tr class="border-b border-gray-200 dark:border-gray-700">
                <th
                  v-for="field in itemSchema"
                  :key="field.key"
                  class="text-left py-3 px-4 font-medium"
                >
                  {{ field.label }}
                </th>
                <th
                  v-for="col in displayColumns"
                  :key="col.key"
                  class="text-left py-3 px-4 font-medium"
                >
                  {{ col.label }}
                </th>
                <th v-if="canEdit || canDelete" class="text-right py-3 px-4 font-medium w-20">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="item in items"
                :key="item.id"
                class="border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800/50"
              >
                <td
                  v-for="field in itemSchema"
                  :key="field.key"
                  class="py-3 px-4"
                >
                  <DataFormField
                    v-if="canEdit && !field.readonly"
                    :schema="field"
                    :model-value="editingValues[item.id]?.[field.key] ?? item[field.key]"
                    :state="getRowState(item.id, field.key)"
                    :error="getRowError(item.id, field.key)"
                    @update:model-value="(val) => handleFieldUpdate(item.id, field, val)"
                    @focus="handleFieldFocus(item.id, field)"
                    @blur="handleFieldBlur(item.id, field)"
                  />
                  <span v-else class="block py-2">
                    {{ field.type === 'select' && field.options
                      ? (field.options.find(o => o.value === item[field.key])?.label ?? item[field.key])
                      : item[field.key] }}
                  </span>
                </td>
                <td
                  v-for="col in displayColumns"
                  :key="col.key"
                  class="py-3 px-4"
                >
                  <component
                    v-if="col.render"
                    :is="col.render(item)"
                    v-bind="typeof col.render(item) === 'object' ? col.render(item).props : {}"
                  >
                    {{ col.render(item)?.text ?? '' }}
                  </component>
                  <span v-else>{{ item[col.key] }}</span>
                </td>
                <td v-if="canEdit || canDelete" class="py-3 px-4 text-right">
                  <UButton
                    v-if="canDelete"
                    icon="i-heroicons-trash"
                    size="xs"
                    variant="ghost"
                    color="red"
                    @click="handleDelete(item)"
                  />
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </UCard>
  </div>
</template>
