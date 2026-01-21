<script setup>
const props = defineProps({
  label: String,
  sublabel: String,
  id: String
})

const isOpen = ref(false)
</script>

<template>
  <UModal v-model="isOpen">
    <UButton icon="i-heroicons-printer" color="neutral" variant="ghost" @click="isOpen = true" />

    <template #content>
      <UCard>
        <template #header>
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-semibold">Label Preview</h3>
            <UButton color="neutral" variant="ghost" icon="i-heroicons-x-mark" @click="isOpen = false" />
          </div>
        </template>

        <div class="p-12 flex flex-col items-center justify-center">
          <!-- Label Mockup -->
          <div class="w-64 h-32 bg-white border-2 border-black p-4 flex gap-4 text-black shadow-lg">
            <div class="w-24 h-24 bg-gray-100 flex items-center justify-center border border-gray-300">
              <UIcon name="i-heroicons-qr-code" class="w-20 h-20" />
            </div>
            <div class="flex-1 flex flex-col justify-center min-w-0">
              <div class="font-bold text-lg leading-tight truncate">{{ label }}</div>
              <div class="text-xs text-gray-600 truncate">{{ sublabel }}</div>
              <div class="mt-2 font-mono text-[10px] bg-gray-100 px-1 rounded">{{ id }}</div>
            </div>
          </div>

          <div class="mt-8 space-y-4 w-full">
            <UFormGroup label="Label Format">
              <USelect :items="['Small (25x12mm)', 'Medium (50x25mm)', 'Large (100x50mm)']" />
            </UFormGroup>
            <UButton label="Print Label" icon="i-heroicons-printer" block color="primary" />
          </div>
        </div>

        <template #footer>
          <div class="text-xs text-gray-500 text-center">
            Integrates with Brother, Dymo, and standard thermal printers.
          </div>
        </template>
      </UCard>
    </template>
  </UModal>
</template>
