<script setup>
const props = defineProps({
  part: {
    type: Object,
    required: true
  }
})

const isOpen = ref(false)
const type = ref('Add')
const quantity = ref(0)
const location = ref(props.part.locations[0]?.name || '')
const note = ref('')

const types = ['Add', 'Set', 'Remove']

const emit = defineEmits(['close', 'save'])

const save = () => {
  // Logic to save adjustment
  emit('save', { type: type.value, quantity: quantity.value, location: location.value, note: note.value })
  isOpen.value = false
}
</script>

<template>
  <UModal v-model="isOpen">
    <UButton label="Adjust Stock" icon="i-heroicons-arrows-right-left" color="primary" @click="isOpen = true" />

    <template #content>
      <UCard>
        <template #header>
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-semibold">Adjust Stock: {{ part.name }}</h3>
            <UButton color="gray" variant="ghost" icon="i-heroicons-x-mark" @click="isOpen = false" />
          </div>
        </template>

        <div class="space-y-4 py-4">
          <UFormGroup label="Adjustment Type">
            <USelect v-model="type" :options="types" />
          </UFormGroup>

          <UFormGroup label="Quantity">
            <UInput v-model.number="quantity" type="number" />
          </UFormGroup>

          <UFormGroup label="Location">
            <USelect v-model="location" :options="part.locations.map(l => l.name)" />
          </UFormGroup>

          <UFormGroup label="Note (Optional)">
            <UTextarea v-model="note" placeholder="Reason for adjustment..." />
          </UFormGroup>
        </div>

        <template #footer>
          <div class="flex justify-end gap-3">
            <UButton label="Cancel" color="gray" variant="ghost" @click="isOpen = false" />
            <UButton label="Save Adjustment" color="primary" @click="save" />
          </div>
        </template>
      </UCard>
    </template>
  </UModal>
</template>
