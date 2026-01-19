<script setup>
const props = defineProps({
  isOpen: Boolean
})

const emit = defineEmits(['update:isOpen', 'import'])

const step = ref(1) // 1: Upload, 2: Mapping, 3: Processing
const file = ref(null)

const columns = ['Designator', 'Quantity', 'MPN', 'Value', 'Footprint', 'Manufacturer']
const mappings = ref({
  designators: 'Designator',
  quantity: 'Quantity',
  mpn: 'MPN'
})

const handleUpload = () => {
  step.value = 2
}

const handleImport = () => {
  step.value = 3
  setTimeout(() => {
    emit('import')
    emit('update:isOpen', false)
    step.value = 1
  }, 1500)
}
</script>

<template>
  <UModal :model-value="isOpen" @update:model-value="emit('update:isOpen', $event)">
    <UCard>
      <template #header>
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-semibold">Import BOM</h3>
          <UButton color="gray" variant="ghost" icon="i-heroicons-x-mark" @click="emit('update:isOpen', false)" />
        </div>
      </template>

      <div class="py-4">
        <!-- Step 1: Upload -->
        <div v-if="step === 1" class="space-y-4">
          <div class="flex flex-col items-center justify-center p-12 border-2 border-dashed border-gray-200 dark:border-gray-800 rounded-lg">
            <UIcon name="i-heroicons-cloud-arrow-up" class="w-12 h-12 mb-2 text-primary-500" />
            <p class="text-sm">Upload CAD export (CSV or TSV)</p>
            <input type="file" class="hidden" id="bom-upload" @change="handleUpload" />
            <UButton label="Choose File" variant="solid" color="primary" class="mt-4" @click="handleUpload" />
          </div>
          <div class="text-xs text-gray-500 text-center">
            Supports Altium, KiCad, Eagle, and custom CSV formats.
          </div>
        </div>

        <!-- Step 2: Mapping -->
        <div v-else-if="step === 2" class="space-y-4">
          <p class="text-sm font-medium">Map your CSV columns to MakerDB fields:</p>
          <div class="space-y-3">
            <UFormGroup label="Designators Column">
              <USelect v-model="mappings.designators" :items="columns" />
            </UFormGroup>
            <UFormGroup label="Quantity Column">
              <USelect v-model="mappings.quantity" :items="columns" />
            </UFormGroup>
            <UFormGroup label="MPN Column">
              <USelect v-model="mappings.mpn" :items="columns" />
            </UFormGroup>
          </div>
        </div>

        <!-- Step 3: Processing -->
        <div v-else-if="step === 3" class="flex flex-col items-center justify-center p-12">
          <UIcon name="i-heroicons-arrow-path" class="w-12 h-12 mb-2 text-primary-500 animate-spin" />
          <p class="text-sm animate-pulse">Matching parts and calculating costs...</p>
        </div>
      </div>

      <template #footer v-if="step === 2">
        <div class="flex justify-end gap-3">
          <UButton label="Back" color="gray" variant="ghost" @click="step = 1" />
          <UButton label="Start Import" color="primary" @click="handleImport" />
        </div>
      </template>
    </UCard>
  </UModal>
</template>
