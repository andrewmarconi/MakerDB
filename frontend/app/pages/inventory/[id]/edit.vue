<script setup lang="ts">
import TagManager from '~/components/Tags/TagManager.vue'
import AttachmentManager from '~/components/Files/AttachmentManager.vue'

definePageMeta({
  title: 'Edit Part'
})

useSeoMeta({
  title: 'Edit Part',
  description: 'Edit part details, specifications, and stock information.'
})

const route = useRoute()
const router = useRouter()
const toast = useToast()

const partId = route.params.id as string

const { data: part, refresh } = await useApiFetch(`/parts/${partId}`)

const tabs = [
  { key: 'basic', label: 'Basic Info', icon: 'i-heroicons-information-circle' },
  { key: 'specs', label: 'Specifications', icon: 'i-heroicons-cpu-chip' },
  { key: 'stock', label: 'Stock Settings', icon: 'i-heroicons-circle-stack' },
  { key: 'attachments', label: 'Attachments', icon: 'i-heroicons-paper-clip' }
]
const activeTab = ref(tabs[0].key)

const partTypes = [
  { label: 'Linked', value: 'linked', description: 'Part with manufacturer info (MPN, datasheet)' },
  { label: 'Local', value: 'local', description: 'Generic part without manufacturer info' },
  { label: 'Meta', value: 'meta', description: 'Group of other parts' },
  { label: 'Sub-assembly', value: 'sub-assembly', description: 'Pre-built assembly linked to project' }
]

const form = ref({
  part_type: 'linked' as string,
  name: '',
  description: '',
  notes: '',
  mpn: '',
  footprint: '',
  manufacturer_id: null as string | null,
  default_storage_id: null as string | null,
  is_default_storage_mandatory: false,
  low_stock_threshold: null as number | null,
  attrition_percent: 0,
  attrition_quantity: 0,
  tags: [] as string[],
  custom_fields: {} as Record<string, string>
})

watch(part, (newPart) => {
  if (newPart) {
    form.value.part_type = (newPart as any).part_type
    form.value.name = (newPart as any).name
    form.value.description = (newPart as any).description || ''
    form.value.notes = (newPart as any).notes || ''
    form.value.mpn = (newPart as any).mpn || ''
    form.value.footprint = (newPart as any).footprint || ''
    form.value.manufacturer_id = (newPart as any).manufacturer?.id || null
    form.value.default_storage_id = (newPart as any).default_storage_id || null
    form.value.is_default_storage_mandatory = (newPart as any).is_default_storage_mandatory || false
    form.value.low_stock_threshold = (newPart as any).low_stock_threshold
    form.value.attrition_percent = (newPart as any).attrition_percent || 0
    form.value.attrition_quantity = (newPart as any).attrition_quantity || 0
    form.value.tags = (newPart as any).tags || []
    form.value.custom_fields = (newPart as any).custom_fields || {}
  }
}, { immediate: true })

const { data: manufacturers, refresh: refreshManufacturers } = await useApiFetch('/core/companies', {
  query: { is_manufacturer: true }
})

const { data: locations } = await useApiFetch('/inventory/locations')

const manufacturerQuery = ref('')
const manufacturerCreating = ref(false)
const showManufacturerForm = ref(false)
const newManufacturer = ref({
  name: '',
  website: ''
})

const manufacturerOptions = computed(() => {
  if (!manufacturers.value) return []
  return manufacturers.value.map((m: any) => ({ label: m.name, value: m.id, website: m.website }))
})

const filteredManufacturers = computed(() => {
  if (!manufacturerQuery.value || !manufacturers.value) return manufacturerOptions.value
  const query = manufacturerQuery.value.toLowerCase()
  return manufacturerOptions.value.filter((m: any) =>
    m.label.toLowerCase().includes(query)
  )
})

const locationOptions = computed(() => {
  if (!locations.value) return []
  return locations.value.map((l: any) => ({ label: l.name, value: l.id }))
})

const customFieldKeys = computed(() => {
  const keys = new Set([...Object.keys(form.value.custom_fields)])
  return Array.from(keys)
})

const customFieldValues = ref<Record<string, string>>({})

watch(() => form.value.custom_fields, (newFields) => {
  Object.keys(newFields).forEach(key => {
    if (!(key in customFieldValues.value)) {
      customFieldValues.value[key] = newFields[key]
    }
  })
}, { immediate: true, deep: true })

const addCustomField = () => {
  const key = `field_${Date.now()}`
  customFieldValues.value[key] = ''
}

const removeCustomField = (key: string) => {
  delete customFieldValues.value[key]
}

const hasLinkedFields = computed(() => form.value.part_type === 'linked')

const isSubmitting = ref(false)
const error = ref<string | null>(null)

async function createManufacturer() {
  if (!newManufacturer.value.name.trim()) return

  manufacturerCreating.value = true
  try {
    const response = await useApiFetch('/core/companies', {
      method: 'POST',
      body: {
        name: newManufacturer.value.name,
        website: newManufacturer.value.website,
        is_manufacturer: true,
        is_vendor: false,
        contacts: []
      }
    })

    await refreshManufacturers()
    form.value.manufacturer_id = (response as any).id
    showManufacturerForm.value = false
    newManufacturer.value = { name: '', website: '' }
    manufacturerQuery.value = ''
    toast.add({ title: 'Manufacturer created' })
  } catch (err: any) {
    toast.add({ title: 'Failed to create manufacturer', description: err.message, color: 'error' })
  } finally {
    manufacturerCreating.value = false
  }
}

async function handleSubmit() {
  isSubmitting.value = true
  error.value = null

  try {
    const payload = {
      part_type: form.value.part_type,
      name: form.value.name,
      description: form.value.description,
      notes: form.value.notes,
      mpn: form.value.mpn,
      footprint: form.value.footprint,
      manufacturer_id: form.value.manufacturer_id,
      default_storage_id: form.value.default_storage_id,
      is_default_storage_mandatory: form.value.is_default_storage_mandatory,
      low_stock_threshold: form.value.low_stock_threshold,
      attrition_percent: form.value.attrition_percent,
      attrition_quantity: form.value.attrition_quantity,
      custom_fields: Object.fromEntries(
        Object.entries(customFieldValues.value).filter(([_, v]) => v && v.trim())
      )
    }

    await useApiFetch(`/parts/${partId}`, {
      method: 'PUT',
      body: payload
    })

    toast.add({ title: 'Part updated successfully' })
    router.push(`/inventory/${partId}`)
  } catch (err: any) {
    error.value = err.data?.detail || err.message || 'Failed to update part'
  } finally {
    isSubmitting.value = false
  }
}

async function handleDelete() {
  if (!confirm('Are you sure you want to delete this part?')) return

  try {
    await useApiFetch(`/parts/${partId}`, { method: 'DELETE' })
    toast.add({ title: 'Part deleted' })
    router.push('/inventory')
  } catch (err: any) {
    toast.add({ title: 'Failed to delete part', description: err.message, color: 'error' })
  }
}

function setActiveTab(tab: any) {
  activeTab.value = tab.key
}
</script>

<template>
  <div v-if="part" class="max-w-4xl mx-auto space-y-6">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-4">
        <UButton variant="ghost" color="gray" icon="i-heroicons-arrow-left" :to="`/inventory/${partId}`" />
        <div>
          <h1 class="text-2xl font-bold">Edit Part</h1>
          <p class="text-gray-500 dark:text-gray-400">Update part details.</p>
        </div>
      </div>
      <UButton icon="i-heroicons-trash" label="Delete" variant="ghost" color="red" @click="handleDelete" />
    </div>

    <UCard>
      <template #header>
        <div class="flex items-center gap-1 p-1 bg-gray-100 dark:bg-gray-800 rounded-lg">
          <button v-for="tab in tabs" :key="tab.key"
            class="flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-colors"
            :class="activeTab === tab.key
              ? 'bg-white dark:bg-gray-700 text-primary shadow-sm'
              : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'"
            @click="setActiveTab(tab)">
            <UIcon :name="tab.icon" class="w-4 h-4" />
            {{ tab.label }}
          </button>
        </div>
      </template>

      <div class="py-6 space-y-6">
        <UAlert v-if="error" color="error" variant="subtle" icon="i-heroicons-exclamation-circle" title="Error"
          :description="error" class="mb-4" />

        <div v-if="activeTab === 'basic'" class="space-y-6">
          <UFormField label="Part Type" required>
            <URadioGroup v-model="form.part_type" :items="partTypes" value-key="value" variant="card"
              orientation="horizontal" />
          </UFormField>

          <UFormField label="Name" required>
            <UInput v-model="form.name" placeholder="e.g., ESP32-WROOM-32 Module" class="w-full" />
          </UFormField>

          <div v-if="hasLinkedFields" class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <UFormField label="Manufacturer Part Number (MPN)">
              <UInput v-model="form.mpn" placeholder="e.g., ESP32-WROOM-32" class="w-full" />
            </UFormField>

            <UFormField label="Manufacturer">
              <div class="space-y-2">
                <UInputMenu v-model="form.manufacturer_id" :items="manufacturerOptions" value-key="value"
                  placeholder="Search or create manufacturer..." searchable :searchable-query="manufacturerQuery"
                  @update:searchable-query="manufacturerQuery = $event" class="w-full">
                  <template #leading>
                    <UIcon name="i-heroicons-magnifying-glass" class="w-4 h-4 text-gray-400" />
                  </template>

                  <template #item="{ item }">
                    <span>{{ item.label }}</span>
                  </template>

                  <template #empty>
                    <div class="p-3">
                      <p class="text-sm text-gray-500 mb-2">No manufacturer found</p>
                      <UButton label="Create" icon="i-heroicons-plus" size="sm" block
                        @click="showManufacturerForm = true" />
                    </div>
                  </template>
                </UInputMenu>

                <div v-if="form.manufacturer_id" class="flex items-center gap-2 text-sm">
                  <UIcon name="i-heroicons-check-circle" class="w-4 h-4 text-green-500" />
                  <span class="text-gray-500">Selected:</span>
                  <span class="font-medium">{{ manufacturerOptions.find((m: any) => m.value === form.manufacturer_id)?.label }}</span>
                </div>
              </div>
            </UFormField>
          </div>

          <UFormField label="Description">
            <UTextarea v-model="form.description" placeholder="Brief description of the part..." class="w-full"
              :rows="3" />
          </UFormField>

          <UFormField label="Category/Tags">
            <TagManager v-model="form.tags" />
          </UFormField>
        </div>

        <div v-if="activeTab === 'specs'" class="space-y-6">
          <UFormField label="Footprint/Package">
            <UInput v-model="form.footprint" placeholder="e.g., SOP-8, 0805, QFP-48" class="w-full" />
          </UFormField>

          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <h3 class="font-medium">Custom Fields</h3>
              <UButton icon="i-heroicons-plus" label="Add Field" variant="soft" color="gray" size="sm"
                @click="addCustomField" />
            </div>

            <div v-if="customFieldKeys.length > 0" class="space-y-3">
              <div v-for="key in customFieldKeys" :key="key" class="flex gap-3">
                <UInput v-model="customFieldValues[key]" placeholder="Field name" class="flex-1" />
                <UInput v-model="customFieldValues[key]" placeholder="Value" class="flex-1" />
                <UButton icon="i-heroicons-trash" variant="ghost" color="red" size="xs"
                  @click="removeCustomField(key)" />
              </div>
            </div>

            <p v-else class="text-sm text-gray-500 italic">No custom fields defined.</p>
          </div>

          <UFormField label="Notes">
            <UTextarea v-model="form.notes" placeholder="Additional notes (Markdown supported)..." class="w-full"
              :rows="4" />
          </UFormField>
        </div>

        <div v-if="activeTab === 'stock'" class="space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <UFormField label="Low Stock Threshold">
              <UInput v-model.number="form.low_stock_threshold" type="number" min="0" placeholder="Optional"
                class="w-full" />
            </UFormField>

            <UFormField label="Default Storage Location">
              <USelect v-model="form.default_storage_id" :items="locationOptions" value-key="value" clearable
                placeholder="Select default location..." class="w-full" />
            </UFormField>
          </div>

          <UFormField label="Storage Mandatory">
            <UCheckbox v-model="form.is_default_storage_mandatory"
              label="Require default storage location for stock entries" />
          </UFormField>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <UFormField label="Attrition (%)">
              <UInput v-model.number="form.attrition_percent" type="number" min="0" max="100" step="0.1"
                placeholder="0" class="w-full" />
            </UFormField>

            <UFormField label="Attrition Qty">
              <UInput v-model.number="form.attrition_quantity" type="number" min="0" placeholder="0"
                class="w-full" />
            </UFormField>
          </div>
        </div>

        <div v-if="activeTab === 'attachments'" class="space-y-4">
          <AttachmentManager :attachments="(part as any).attachments || []" :part-id="partId" />
        </div>
      </div>
    </UCard>

    <div class="flex items-center justify-between">
      <UButton v-if="activeTab !== 'basic'" label="Back" icon="i-heroicons-arrow-left" variant="ghost" color="gray"
        @click="() => { const idx = tabs.findIndex(t => t.key === activeTab); if (idx > 0) activeTab = tabs[idx - 1].key }" />
      <div v-else></div>

      <div class="flex gap-3">
        <UButton label="Cancel" color="gray" variant="ghost" :to="`/inventory/${partId}`" />
        <UButton v-if="activeTab !== 'attachments'" label="Next" icon="i-heroicons-arrow-right" icon-end color="primary"
          @click="() => { const idx = tabs.findIndex(t => t.key === activeTab); if (idx < tabs.length - 1) activeTab = tabs[idx + 1].key }" />
        <UButton v-else label="Save Changes" icon="i-heroicons-check" color="primary" :loading="isSubmitting"
          @click="handleSubmit" />
      </div>
    </div>

    <UModal v-model="showManufacturerForm">
      <UCard>
        <template #header>
          <h3 class="text-lg font-semibold">Create New Manufacturer</h3>
        </template>

        <div class="space-y-4 py-4">
          <UFormField label="Name" required>
            <UInput v-model="newManufacturer.name" placeholder="e.g., Texas Instruments" class="w-full" />
          </UFormField>

          <UFormField label="Website (Optional)">
            <UInput v-model="newManufacturer.website" placeholder="https://www.ti.com" class="w-full" />
          </UFormField>
        </div>

        <template #footer>
          <div class="flex justify-end gap-3">
            <UButton label="Cancel" color="gray" variant="ghost" @click="showManufacturerForm = false" />
            <UButton label="Create Manufacturer" icon="i-heroicons-plus" :loading="manufacturerCreating"
              :disabled="!newManufacturer.name.trim()" @click="createManufacturer" />
          </div>
        </template>
      </UCard>
    </UModal>
  </div>

  <div v-else class="flex items-center justify-center py-12">
    <UIcon name="i-heroicons-arrow-path" class="w-8 h-8 animate-spin text-gray-400" />
  </div>
</template>
