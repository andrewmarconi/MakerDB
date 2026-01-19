<script setup>
const props = defineProps({
  order: {
    type: Object,
    required: true
  }
})

const isOpen = ref(false)
const step = ref(1) // 1: Verify Quantities, 2: Assign Locations, 3: Confirm

const receivedItems = ref(props.order.items.map(item => ({
  ...item,
  receivedQty: item.quantity,
  location: 'b01-a4', // Default location placeholder
  lotControl: true
})))

const emit = defineEmits(['receive'])

const nextStep = () => step.value++
const prevStep = () => step.value--

const confirmReceipt = () => {
  emit('receive', receivedItems.value)
  isOpen.value = false
  step.value = 1
}
</script>

<template>
  <UModal v-model="isOpen">
    <UButton label="Receive Items" icon="i-heroicons-archive-box" color="green" @click="isOpen = true" />

    <template #content>
      <UCard>
        <template #header>
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-semibold">Receive Order: {{ order.id }}</h3>
            <UButton color="gray" variant="ghost" icon="i-heroicons-x-mark" @click="isOpen = false" />
          </div>
          <div class="mt-4">
            <UStepper :model-value="step" :items="[{ label: 'Quantities' }, { label: 'Locations' }, { label: 'Confirm' }]" />
          </div>
        </template>

        <div class="py-4 space-y-4">
          <!-- Step 1: Quantities -->
          <div v-if="step === 1" class="space-y-4">
            <p class="text-sm text-gray-500">Verify the quantities received for each item.</p>
            <div v-for="item in receivedItems" :key="item.id" class="flex items-center gap-4 p-3 bg-gray-50 dark:bg-gray-900 rounded-lg">
              <div class="flex-1">
                <div class="font-medium text-sm">{{ item.mpn }}</div>
                <div class="text-xs text-gray-500">{{ item.description }}</div>
              </div>
              <div class="w-24">
                <UInput v-model.number="item.receivedQty" type="number" size="sm" :trailing-text="` / ${item.quantity}`" />
              </div>
            </div>
          </div>

          <!-- Step 2: Locations -->
          <div v-else-if="step === 2" class="space-y-4">
            <p class="text-sm text-gray-500">Assign received items to storage locations.</p>
            <div v-for="item in receivedItems" :key="item.id" class="flex items-center gap-4 p-3 bg-gray-50 dark:bg-gray-900 rounded-lg">
              <div class="flex-1">
                <div class="font-medium text-sm">{{ item.mpn }} ({{ item.receivedQty }} pcs)</div>
              </div>
              <div class="w-32">
                <USelect v-model="item.location" :items="['b01-a4', 'b01-a5', 'b02-c1']" size="sm" />
              </div>
            </div>
          </div>

          <!-- Step 3: Confirm -->
          <div v-else-if="step === 3" class="space-y-4">
            <div class="flex flex-col items-center justify-center p-8 text-center">
              <UIcon name="i-heroicons-check-badge" class="w-16 h-16 text-green-500 mb-4" />
              <h4 class="text-lg font-bold">Ready to Receive</h4>
              <p class="text-sm text-gray-500 mt-2">
                This will add {{ receivedItems.length }} line items to inventory and generate lot tracking records.
              </p>
            </div>
          </div>
        </div>

        <template #footer>
          <div class="flex justify-between gap-3">
            <UButton v-if="step > 1" label="Back" color="gray" variant="ghost" @click="prevStep" />
            <div v-else />
            
            <div class="flex gap-3">
              <UButton label="Cancel" color="gray" variant="ghost" @click="isOpen = false" />
              <UButton v-if="step < 3" label="Next" color="primary" @click="nextStep" />
              <UButton v-else label="Confirm Receipt" color="green" @click="confirmReceipt" />
            </div>
          </div>
        </template>
      </UCard>
    </template>
  </UModal>
</template>
