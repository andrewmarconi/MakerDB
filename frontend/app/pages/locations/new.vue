<script setup lang="ts">
definePageMeta({
  title: 'Add New Location'
})

useSeoMeta({
  title: 'Add New Location',
  description: 'Create a new storage location in your hierarchy.'
})

const router = useRouter()

// Mode selection
const mode = ref<CreateMode>('single')

const modeOptions = [
  { label: 'Single', value: 'single', description: 'Create one location', icon: 'i-heroicons-square-2-stack' },
  { label: 'Row', value: 'row', description: 'Create a sequence (A-Z or 1-20)', icon: 'i-heroicons-bars-3' },
  { label: 'Grid', value: 'grid', description: 'Create a grid (rows x columns)', icon: 'i-heroicons-squares-2x2' }
]

// Fetch existing locations for parent selection and conflict checking
const { data: locations } = await useApiFetch('/inventory/locations')

const parentOptions = computed(() => {
  if (!locations.value) return [{ label: 'None (Top Level)', value: null }]
  return [
    { label: 'None (Top Level)', value: null },
    ...locations.value.map((loc: any) => ({ label: loc.name, value: loc.id }))
  ]
})

// Single mode form
const singleForm = ref({
  name: '',
  description: '',
  parent_id: null as string | null
})

// Row mode form
const rowForm = ref({
  prefix: '',
  rangeType: 'letters' as RangeType,
  rangeStart: 'A',
  rangeEnd: 'Z',
  parent_id: null as string | null
})

// Grid mode form
const gridForm = ref({
  prefix: '',
  rowRangeType: 'numbers' as RangeType,
  rowStart: '1',
  rowEnd: '5',
  colRangeType: 'letters' as RangeType,
  colStart: 'A',
  colEnd: 'F',
  parent_id: null as string | null
})

// Generate range helper
function generateRange(type: RangeType, start: string, end: string): string[] {
  if (type === 'letters') {
    const startCode = start.toUpperCase().charCodeAt(0)
    const endCode = end.toUpperCase().charCodeAt(0)
    if (startCode > endCode || startCode < 65 || endCode > 90) return []
    return Array.from({ length: endCode - startCode + 1 }, (_, i) => String.fromCharCode(startCode + i))
  } else {
    const startNum = parseInt(start)
    const endNum = parseInt(end)
    if (isNaN(startNum) || isNaN(endNum) || startNum > endNum || startNum < 0) return []
    return Array.from({ length: endNum - startNum + 1 }, (_, i) => String(startNum + i))
  }
}

// Preview names for row mode
const rowPreviewNames = computed(() => {
  const range = generateRange(rowForm.value.rangeType, rowForm.value.rangeStart, rowForm.value.rangeEnd)
  return range.map(r => `${rowForm.value.prefix}${r}`)
})

// Preview names for grid mode
const gridPreviewNames = computed(() => {
  const rows = generateRange(gridForm.value.rowRangeType, gridForm.value.rowStart, gridForm.value.rowEnd)
  const cols = generateRange(gridForm.value.colRangeType, gridForm.value.colStart, gridForm.value.colEnd)
  const names: string[] = []
  for (const row of rows) {
    for (const col of cols) {
      names.push(`${gridForm.value.prefix}${row}${col}`)
    }
  }
  return names
})

// Check for conflicts
const existingNames = computed(() => {
  if (!locations.value) return new Set<string>()
  return new Set(locations.value.map((loc: any) => loc.name.toLowerCase()))
})

const rowConflicts = computed(() => {
  return rowPreviewNames.value.filter(name => existingNames.value.has(name.toLowerCase()))
})

const gridConflicts = computed(() => {
  return gridPreviewNames.value.filter(name => existingNames.value.has(name.toLowerCase()))
})

// Submission
const isSubmitting = ref(false)
const error = ref<string | null>(null)

async function handleSubmit() {
  isSubmitting.value = true
  error.value = null

  try {
    if (mode.value === 'single') {
      await useApiFetch('/inventory/locations', {
        method: 'POST',
        body: {
          name: singleForm.value.name,
          description: singleForm.value.description
        }
      })
    } else {
      // Bulk create for row/grid modes
      const names = mode.value === 'row' ? rowPreviewNames.value : gridPreviewNames.value
      const parentId = mode.value === 'row' ? rowForm.value.parent_id : gridForm.value.parent_id

      for (const name of names) {
        await useApiFetch('/inventory/locations', {
          method: 'POST',
          body: { name, description: '' }
        })
      }
    }

    router.push('/locations')
  } catch (err: any) {
    error.value = err.message || 'Failed to create location(s)'
  } finally {
    isSubmitting.value = false
  }
}

// Validation
const isValid = computed(() => {
  if (mode.value === 'single') {
    return singleForm.value.name.trim().length > 0
  } else if (mode.value === 'row') {
    return rowForm.value.prefix.trim().length > 0 && rowPreviewNames.value.length > 0
  } else {
    return gridForm.value.prefix.trim().length > 0 && gridPreviewNames.value.length > 0
  }
})
</script>

<template>
  <div class="max-w-4xl mx-auto space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold">Create Storage Location</h1>
        <p class="text-gray-500 dark:text-gray-400">Add new storage locations to organize your inventory.</p>
      </div>
      <UButton icon="i-heroicons-x-mark" variant="ghost" color="neutral" to="/locations" />
    </div>

    <!-- Mode Selection -->
    <UCard>
      <template #header>
        <h3 class="font-semibold">Creation Mode</h3>
      </template>

      <URadioGroup v-model="mode" :items="modeOptions" value-key="value" variant="card" orientation="horizontal" />
    </UCard>

    <!-- Single Mode Form -->
    <UCard v-if="mode === 'single'">
      <template #header>
        <h3 class="font-semibold">Location Details</h3>
      </template>

      <div class="space-y-4">
        <UFormField label="Name" required>
          <UInput v-model="singleForm.name" placeholder="e.g., Shelf A, Drawer 1, Box 12" class="w-full" />
        </UFormField>

        <UFormField label="Description">
          <UTextarea v-model="singleForm.description" placeholder="Optional description..." class="w-full" :rows="3" />
        </UFormField>

        <UFormField label="Parent Location">
          <USelect v-model="singleForm.parent_id" :items="parentOptions" value-key="value" class="w-full" />
        </UFormField>
      </div>
    </UCard>

    <!-- Row Mode Form -->
    <UCard v-if="mode === 'row'">
      <template #header>
        <h3 class="font-semibold">Sequence Configuration</h3>
      </template>

      <div class="space-y-4">
        <UFormField label="Prefix" required description="Text that appears before each number/letter">
          <UInput v-model="rowForm.prefix" placeholder="e.g., Box-, Shelf-A-, Drawer" class="w-full" />
        </UFormField>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <UFormField label="Range Type">
            <USelect v-model="rowForm.rangeType" :items="[
              { label: 'Letters (A-Z)', value: 'letters' },
              { label: 'Numbers (1-99)', value: 'numbers' }
            ]" value-key="value" class="w-full" />
          </UFormField>

          <UFormField label="Start">
            <UInput v-model="rowForm.rangeStart" :placeholder="rowForm.rangeType === 'letters' ? 'A' : '1'"
              class="w-full" />
          </UFormField>

          <UFormField label="End">
            <UInput v-model="rowForm.rangeEnd" :placeholder="rowForm.rangeType === 'letters' ? 'Z' : '20'"
              class="w-full" />
          </UFormField>
        </div>

        <UFormField label="Parent Location">
          <USelect v-model="rowForm.parent_id" :items="parentOptions" value-key="value" class="w-full" />
        </UFormField>
      </div>
    </UCard>

    <!-- Grid Mode Form -->
    <UCard v-if="mode === 'grid'">
      <template #header>
        <h3 class="font-semibold">Grid Configuration</h3>
      </template>

      <div class="space-y-4">
        <UFormField label="Prefix" required description="Text that appears before row/column identifiers">
          <UInput v-model="gridForm.prefix" placeholder="e.g., Shelf-, Cabinet-, Bin-" class="w-full" />
        </UFormField>

        <!-- Row Range -->
        <div class="p-4 bg-gray-50 dark:bg-gray-900 rounded-lg space-y-3">
          <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300">Row Range</h4>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <UFormField label="Type">
              <USelect v-model="gridForm.rowRangeType" :items="[
                { label: 'Letters', value: 'letters' },
                { label: 'Numbers', value: 'numbers' }
              ]" value-key="value" class="w-full" />
            </UFormField>

            <UFormField label="Start">
              <UInput v-model="gridForm.rowStart" :placeholder="gridForm.rowRangeType === 'letters' ? 'A' : '1'"
                class="w-full" />
            </UFormField>

            <UFormField label="End">
              <UInput v-model="gridForm.rowEnd" :placeholder="gridForm.rowRangeType === 'letters' ? 'E' : '5'"
                class="w-full" />
            </UFormField>
          </div>
        </div>

        <!-- Column Range -->
        <div class="p-4 bg-gray-50 dark:bg-gray-900 rounded-lg space-y-3">
          <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300">Column Range</h4>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <UFormField label="Type">
              <USelect v-model="gridForm.colRangeType" :items="[
                { label: 'Letters', value: 'letters' },
                { label: 'Numbers', value: 'numbers' }
              ]" value-key="value" class="w-full" />
            </UFormField>

            <UFormField label="Start">
              <UInput v-model="gridForm.colStart" :placeholder="gridForm.colRangeType === 'letters' ? 'A' : '1'"
                class="w-full" />
            </UFormField>

            <UFormField label="End">
              <UInput v-model="gridForm.colEnd" :placeholder="gridForm.colRangeType === 'letters' ? 'F' : '6'"
                class="w-full" />
            </UFormField>
          </div>
        </div>

        <UFormField label="Parent Location">
          <USelect v-model="gridForm.parent_id" :items="parentOptions" value-key="value" class="w-full" />
        </UFormField>
      </div>
    </UCard>

    <!-- Preview Panel -->
    <UCard v-if="mode !== 'single'">
      <template #header>
        <div class="flex items-center justify-between">
          <h3 class="font-semibold">Preview</h3>
          <UBadge :color="(mode === 'row' ? rowConflicts : gridConflicts).length > 0 ? 'warning' : 'success'"
            variant="subtle">
            {{ mode === 'row' ? rowPreviewNames.length : gridPreviewNames.length }} locations
          </UBadge>
        </div>
      </template>

      <!-- Conflicts Warning -->
      <UAlert v-if="(mode === 'row' ? rowConflicts : gridConflicts).length > 0" color="warning" variant="subtle"
        icon="i-heroicons-exclamation-triangle" title="Naming Conflicts Detected" class="mb-4"
        :description="`${(mode === 'row' ? rowConflicts : gridConflicts).length} location(s) already exist: ${(mode === 'row' ? rowConflicts : gridConflicts).slice(0, 3).join(', ')}${(mode === 'row' ? rowConflicts : gridConflicts).length > 3 ? '...' : ''}`" />

      <!-- Row Preview -->
      <div v-if="mode === 'row'" class="flex flex-wrap gap-2">
        <template v-for="(name, idx) in rowPreviewNames.slice(0, 30)" :key="idx">
          <UBadge :color="rowConflicts.includes(name) ? 'warning' : 'neutral'" variant="subtle">
            {{ name }}
          </UBadge>
        </template>
        <UBadge v-if="rowPreviewNames.length > 30" color="neutral" variant="outline">
          ... and {{ rowPreviewNames.length - 30 }} more
        </UBadge>
      </div>

      <!-- Grid Preview -->
      <div v-if="mode === 'grid'">
        <div class="overflow-x-auto">
          <div class="inline-grid gap-1" :style="{
            gridTemplateColumns: `repeat(${generateRange(gridForm.colRangeType, gridForm.colStart, gridForm.colEnd).length}, minmax(0, 1fr))`
          }">
            <template v-for="(name, idx) in gridPreviewNames.slice(0, 64)" :key="idx">
              <div class="px-2 py-1 text-xs font-mono rounded text-center"
                :class="gridConflicts.includes(name) ? 'bg-warning-100 dark:bg-warning-900 text-warning-700 dark:text-warning-300' : 'bg-gray-100 dark:bg-gray-800'">
                {{ name }}
              </div>
            </template>
          </div>
        </div>
        <p v-if="gridPreviewNames.length > 64" class="text-sm text-gray-500 mt-2">
          ... and {{ gridPreviewNames.length - 64 }} more locations
        </p>
      </div>

      <div v-if="(mode === 'row' ? rowPreviewNames : gridPreviewNames).length === 0"
        class="text-center py-8 text-gray-500">
        <UIcon name="i-heroicons-square-3-stack-3d" class="w-8 h-8 mx-auto mb-2 opacity-50" />
        <p>Configure the range to see preview</p>
      </div>
    </UCard>

    <!-- Error Display -->
    <UAlert v-if="error" color="error" variant="subtle" icon="i-heroicons-exclamation-circle" title="Error"
      :description="error" />

    <!-- Actions -->
    <div class="flex items-center justify-end gap-3">
      <UButton label="Cancel" color="neutral" variant="ghost" to="/locations" />
      <UButton :label="mode === 'single' ? 'Create Location' : `Create ${mode === 'row' ? rowPreviewNames.length : gridPreviewNames.length} Locations`"
        color="primary" :loading="isSubmitting" :disabled="!isValid || isSubmitting" @click="handleSubmit" />
    </div>
  </div>
</template>
