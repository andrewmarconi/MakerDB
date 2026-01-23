<script setup lang="ts">
const props = defineProps({
  part: {
    type: Object as PropType<any>,
    required: true
  }
})

const emit = defineEmits(['close', 'saved'])

const isOpen = ref(false)
const isSubmitting = ref(false)
const error = ref<string | null>(null)

const adjustmentType = ref<'add' | 'set' | 'remove'>('add')
const quantity = ref(0)
const locationId = ref('')
const lotId = ref('' as string | null)
const note = ref('')

const adjustmentTypes = [
  { label: 'Add Stock', value: 'add', icon: 'i-heroicons-plus' },
  { label: 'Set Stock', value: 'set', icon: 'i-heroicons-arrow-right' },
  { label: 'Remove Stock', value: 'remove', icon: 'i-heroicons-minus' }
]

const { data: locations } = await useApiFetch('/inventory/locations')
const { data: lots } = await useApiFetch('/inventory/lots')

const locationOptions = computed(() => {
  if (!locations.value) return []
  return (locations.value as any[]).map(loc => ({ label: loc.name, value: loc.id }))
})

const lotOptions = computed(() => {
  if (!lots.value) return []
  return (lots.value as any[]).map(lot => ({ label: lot.name, value: lot.id }))
})

const existingStock = computed(() => {
  if (!props.part?.locations || !locationId.value) return 0
  const loc = (props.part.locations as any[]).find((l: any) => l.id === locationId.value)
  return loc?.quantity || 0
})

const previewQuantity = computed(() => {
  if (adjustmentType.value === 'add') return existingStock.value + quantity.value
  if (adjustmentType.value === 'remove') return Math.max(0, existingStock.value - quantity.value)
  return quantity.value
})

function resetForm() {
  adjustmentType.value = 'add'
  quantity.value = 0
  locationId.value = props.part.locations?.[0]?.id || ''
  lotId.value = null
  note.value = ''
  error.value = null
}

async function handleSubmit() {
  if (!locationId.value || quantity.value <= 0) return

  isSubmitting.value = true
  error.value = null

  try {
    if (adjustmentType.value === 'add') {
      await useApiFetch('/inventory/stock', {
        method: 'POST',
        body: {
          part_id: props.part.id,
          storage_id: locationId.value,
          quantity: quantity.value,
          lot_id: lotId.value,
          status: null,
          custom_fields: note.value ? { note: note.value } : {}
        }
      })
    } else if (adjustmentType.value === 'set') {
      const existingEntry = (props.part.locations as any[]).find(l => l.id === locationId.value)
      if (existingEntry) {
        await useApiFetch(`/inventory/stock/${existingEntry.stock_id}`, {
          method: 'PUT',
          body: {
            quantity: quantity.value,
            lot_id: lotId.value
          }
        })
      } else {
        await useApiFetch('/inventory/stock', {
          method: 'POST',
          body: {
            part_id: props.part.id,
            storage_id: locationId.value,
            quantity: quantity.value,
            lot_id: lotId.value
          }
        })
      }
    } else if (adjustmentType.value === 'remove') {
      const existingEntry = (props.part.locations as any[]).find(l => l.id === locationId.value)
      if (existingEntry) {
        if (existingEntry.quantity <= quantity.value) {
          await useApiFetch(`/inventory/stock/${existingEntry.stock_id}`, { method: 'DELETE' })
        } else {
          await useApiFetch(`/inventory/stock/${existingEntry.stock_id}`, {
            method: 'PUT',
            body: {
              quantity: existingEntry.quantity - quantity.value
            }
          })
        }
      }
    }

    emit('saved')
    isOpen.value = false
    resetForm()
  } catch (err: any) {
    error.value = err.data?.detail || err.message || 'Failed to adjust stock'
  } finally {
    isSubmitting.value = false
  }
}

watch(isOpen, (val) => {
  if (val) resetForm()
})
</script>

<template>
  <UModal v-model:open="isOpen">
    <template #body>
      <UCard>
        <template #header>
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-semibold">Adjust Stock: {{ part.name }}</h3>
            <UButton color="neutral" variant="ghost" icon="i-heroicons-x-mark" @click="isOpen = false" />
          </div>
        </template>

        <div class="space-y-4 py-4">
          <UAlert v-if="error" color="error" variant="subtle" icon="i-heroicons-exclamation-circle"
            :description="error" class="mb-4" />

          <UFormField label="Adjustment Type">
            <URadioGroup v-model="adjustmentType" :items="adjustmentTypes" value-key="value" variant="card"
              orientation="horizontal" />
          </UFormField>

          <div class="grid grid-cols-2 gap-4">
            <UFormField label="Location" required>
              <USelect v-model="locationId" :items="locationOptions" value-key="value" class="w-full" />
            </UFormField>

            <UFormField label="Lot/Batch">
              <USelect v-model="lotId" :items="lotOptions" value-key="value" clearable placeholder="Optional"
                class="w-full" />
            </UFormField>
          </div>

          <UFormField label="Quantity" required>
            <UInput v-model.number="quantity" type="number" min="0" class="w-full" />
          </UFormField>

          <div v-if="existingStock > 0" class="p-3 bg-gray-50 dark:bg-gray-900 rounded text-sm">
            <div class="flex justify-between">
              <span class="text-gray-500">Current stock:</span>
              <span class="font-mono">{{ existingStock }}</span>
            </div>
            <div class="flex justify-between mt-1">
              <span class="text-gray-500">After adjustment:</span>
              <span class="font-mono font-medium"
                :class="previewQuantity === 0 ? 'text-red-500' : 'text-green-500'">{{ previewQuantity }}</span>
            </div>
          </div>

          <UFormField label="Note (Optional)">
            <UTextarea v-model="note" placeholder="Reason for adjustment..." class="w-full" :rows="2" />
          </UFormField>
        </div>

        <template #footer>
          <div class="flex justify-end gap-3">
            <UButton label="Cancel" color="neutral" variant="ghost" @click="isOpen = false" />
            <UButton :label="adjustmentType === 'add' ? 'Add Stock' : adjustmentType === 'set' ? 'Set Stock' : 'Remove Stock'"
              :color="adjustmentType === 'remove' ? 'error' : 'primary'" :loading="isSubmitting" :disabled="!locationId || quantity < 0"
              @click="handleSubmit" />
          </div>
        </template>
      </UCard>
    </template>
  </UModal>

  <UButton label="Adjust Stock" icon="i-heroicons-arrows-right-left" color="primary" @click="isOpen = true" />
</template>
