<script setup lang="ts">
definePageMeta({
  title: 'Import BOM'
})

useSeoMeta({
  title: 'Import BOM',
  description: 'Import a Bill of Materials from a CSV file.'
})

const route = useRoute()
const router = useRouter()
const toast = useToast()

const projectId = route.params.id as string

const { data: project } = await useApiFetch(`/projects/${projectId}`)

const step = ref(1)
const file = ref<File | null>(null)
const parsedData = ref<any[]>([])
const columnMapping = ref({
  reference: '',
  quantity: 'quantity',
  part_number: 'part_number',
  description: 'description'
})
const isProcessing = ref(false)
const error = ref<string | null>(null)

const availableColumns = computed(() => {
  if (parsedData.value.length === 0) return []
  return Object.keys(parsedData.value[0])
})

const previewData = computed(() => {
  return parsedData.value.slice(0, 10)
})

const matchedCount = computed(() => {
  return parsedData.value.filter(row => row._matched).length
})

const unmatchedCount = computed(() => {
  return parsedData.value.filter(row => !row._matched).length
})

function handleFileSelect(event: Event) {
  const target = event.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    file.value = target.files[0]
    parseFile()
  }
}

async function parseFile() {
  if (!file.value) return

  isProcessing.value = true
  error.value = null

  try {
    const text = await file.value.text()
    const lines = text.trim().split('\n')
    const headers = lines[0].split(',').map(h => h.trim().toLowerCase().replace(/['"]/g, ''))

    parsedData.value = lines.slice(1).map((line, index) => {
      const values = line.split(',').map(v => v.trim().replace(/['"]/g, ''))
      const row: any = {}
      headers.forEach((header, i) => {
        row[header] = values[i] || ''
      })
      row._original = line
      row._index = index + 1
      return row
    })

    autoMapColumns(headers)
    step.value = 2
  } catch (err: any) {
    error.value = 'Failed to parse CSV file: ' + err.message
  } finally {
    isProcessing.value = false
  }
}

function autoMapColumns(headers: string[]) {
  const mappings: Record<string, string[]> = {
    reference: ['reference', 'designator', 'designators', 'ref', 'refs', 'part ref', 'designator(s)'],
    quantity: ['quantity', 'qty', 'count', 'amount', 'num'],
    part_number: ['part_number', 'part number', 'mpn', 'manufacturer part number', 'pn', 'p/n', 'part #'],
    description: ['description', 'desc', 'item description', 'part description']
  }

  Object.entries(mappings).forEach(([key, aliases]) => {
    const match = headers.find(h => aliases.includes(h.toLowerCase()))
    if (match) {
      columnMapping.value[key as keyof typeof columnMapping.value] = match
    }
  })
}

async function previewAndMatch() {
  if (!columnMapping.value.quantity) {
    error.value = 'Please map the quantity column'
    return
  }

  isProcessing.value = true
  error.value = null

  try {
    const itemsToMatch = parsedData.value.map(row => ({
      reference: row[columnMapping.value.reference] || null,
      quantity: parseInt(row[columnMapping.value.quantity]) || 1,
      part_number: row[columnMapping.value.part_number] || null,
      description: row[columnMapping.value.description] || null
    }))

    const matchResults = await useApiFetch(`/projects/${projectId}/bom/match`, {
      method: 'POST',
      body: itemsToMatch
    })

    parsedData.value = parsedData.value.map((row, index) => {
      const match = (matchResults as any)[index]
      return {
        ...row,
        _matched: match?.matched || false,
        _part_id: match?.part_id || null,
        _part_name: match?.part_name || null
      }
    })

    step.value = 3
  } catch (err: any) {
    error.value = 'Failed to match parts: ' + (err.data?.detail || err.message)
  } finally {
    isProcessing.value = false
  }
}

async function handleImport() {
  isProcessing.value = true
  error.value = null

  try {
    const formData = new FormData()
    formData.append('file', file.value!)

    await useApiFetch(`/projects/${projectId}/bom/import`, {
      method: 'POST',
      body: formData
    })

    toast.add({ title: 'BOM imported successfully' })
    router.push(`/projects/${projectId}`)
  } catch (err: any) {
    error.value = 'Failed to import BOM: ' + (err.data?.detail || err.message)
  } finally {
    isProcessing.value = false
  }
}

function reset() {
  file.value = null
  parsedData.value = []
  step.value = 1
  error.value = null
}
</script>

<template>
  <div class="max-w-4xl mx-auto space-y-6">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-4">
        <UButton variant="ghost" color="gray" icon="i-heroicons-arrow-left" :to="`/projects/${projectId}`" />
        <div>
          <h1 class="text-2xl font-bold">Import BOM</h1>
          <p class="text-gray-500 dark:text-gray-400">Upload a CSV file to import into {{ (project as any)?.name }}</p>
        </div>
      </div>
    </div>

    <UAlert v-if="error" color="error" variant="subtle" icon="i-heroicons-exclamation-circle" title="Error"
      :description="error" class="mb-4" />

    <UCard>
      <template #header>
        <div class="flex items-center gap-2">
          <UBadge :color="step >= 1 ? 'primary' : 'gray'" variant="subtle">1. Upload</UBadge>
          <UIcon name="i-heroicons-chevron-right" class="w-4 h-4 text-gray-400" />
          <UBadge :color="step >= 2 ? 'primary' : 'gray'" variant="subtle">2. Map Columns</UBadge>
          <UIcon name="i-heroicons-chevron-right" class="w-4 h-4 text-gray-400" />
          <UBadge :color="step >= 3 ? 'primary' : 'gray'" variant="subtle">3. Review & Import</UBadge>
        </div>
      </template>

      <div class="py-6">
        <div v-if="step === 1" class="space-y-6">
          <div class="border-2 border-dashed border-gray-200 dark:border-gray-700 rounded-lg p-12 text-center hover:border-primary-500 transition-colors">
            <UIcon name="i-heroicons-document-arrow-up" class="w-12 h-12 mx-auto mb-4 text-gray-400" />
            <p class="text-lg font-medium mb-2">Upload your BOM CSV file</p>
            <p class="text-sm text-gray-500 mb-4">Supports CSV files exported from KiCad, Eagle, Altium, etc.</p>
            <UButton label="Select File" icon="i-heroicons-folder" color="primary"
              @click="$refs.fileInput.click()" />
            <input ref="fileInput" type="file" accept=".csv,.txt" class="hidden" @change="handleFileSelect" />
          </div>

          <div v-if="isProcessing" class="text-center py-8">
            <UIcon name="i-heroicons-arrow-path" class="w-8 h-8 animate-spin text-primary mx-auto mb-2" />
            <p class="text-gray-500">Processing file...</p>
          </div>
        </div>

        <div v-if="step === 2" class="space-y-6">
          <p class="text-sm text-gray-500">Map the columns from your CSV to the expected fields.</p>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <UFormField label="Reference/Designator Column">
              <USelect v-model="columnMapping.reference" :items="availableColumns" value-key="value" clearable
                placeholder="(Optional) Column with designators like R1, C2" class="w-full" />
            </UFormField>

            <UFormField label="Quantity Column" required>
              <USelect v-model="columnMapping.quantity" :items="availableColumns" value-key="value"
                placeholder="Column with quantities" class="w-full" />
            </UFormField>

            <UFormField label="Part Number Column">
              <USelect v-model="columnMapping.part_number" :items="availableColumns" value-key="value" clearable
                placeholder="(Optional) MPN column for matching" class="w-full" />
            </UFormField>

            <UFormField label="Description Column">
              <USelect v-model="columnMapping.description" :items="availableColumns" value-key="value" clearable
                placeholder="(Optional) Description column" class="w-full" />
            </UFormField>
          </div>

          <div class="flex justify-between pt-4">
            <UButton label="Back" color="gray" variant="ghost" @click="reset" />
            <UButton label="Preview & Match Parts" icon="i-heroicons-sparkles" color="primary"
              :loading="isProcessing" @click="previewAndMatch" />
          </div>
        </div>

        <div v-if="step === 3" class="space-y-6">
          <div class="grid grid-cols-2 gap-4">
            <UCard class="bg-green-50 dark:bg-green-900/10 border-green-200 dark:border-green-800">
              <div class="text-2xl font-bold text-green-600 dark:text-green-400">{{ matchedCount }}</div>
              <div class="text-sm text-green-600 dark:text-green-400">Matched Parts</div>
            </UCard>
            <UCard class="bg-amber-50 dark:bg-amber-900/10 border-amber-200 dark:border-amber-800">
              <div class="text-2xl font-bold text-amber-600 dark:text-amber-400">{{ unmatchedCount }}</div>
              <div class="text-sm text-amber-600 dark:text-amber-400">Unmatched Items</div>
            </UCard>
          </div>

          <div class="overflow-x-auto">
            <table class="w-full text-sm">
              <thead>
                <tr class="border-b border-gray-200 dark:border-gray-700">
                  <th class="text-left py-2 px-3 font-medium">Ref</th>
                  <th class="text-left py-2 px-3 font-medium">Qty</th>
                  <th class="text-left py-2 px-3 font-medium">Part Number</th>
                  <th class="text-left py-2 px-3 font-medium">Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="row in previewData" :key="row._index"
                  class="border-b border-gray-100 dark:border-gray-800">
                  <td class="py-2 px-3 font-mono">{{ row[columnMapping.reference] || '-' }}</td>
                  <td class="py-2 px-3">{{ row[columnMapping.quantity] }}</td>
                  <td class="py-2 px-3 font-mono">{{ row[columnMapping.part_number] || '-' }}</td>
                  <td class="py-2 px-3">
                    <UBadge v-if="row._matched" color="green" size="sm">Matched</UBadge>
                    <UBadge v-else color="amber" size="sm">Unmatched</UBadge>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <p v-if="parsedData.length > 10" class="text-sm text-gray-500 text-center">
            Showing first 10 of {{ parsedData.length }} items
          </p>

          <div class="flex justify-between pt-4">
            <UButton label="Back" color="gray" variant="ghost" @click="step = 2" />
            <UButton label="Import BOM" icon="i-heroicons-arrow-down-tray" color="primary"
              :loading="isProcessing" @click="handleImport" />
          </div>
        </div>
      </div>
    </UCard>
  </div>
</template>
