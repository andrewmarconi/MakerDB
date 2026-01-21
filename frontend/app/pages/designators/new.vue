<script setup lang="ts">
definePageMeta({
  title: 'Add New Designator'
})

useSeoMeta({
  title: 'Add New Designator',
  description: 'Add a new component designator prefix to your database.'
})

const router = useRouter()
const toast = useToast()

const form = ref({
  code: '',
  name: ''
})

const isSubmitting = ref(false)
const error = ref<string | null>(null)

async function handleSubmit() {
  if (!form.value.code.trim()) {
    error.value = 'Code is required'
    return
  }
  if (!form.value.name.trim()) {
    error.value = 'Name is required'
    return
  }

  isSubmitting.value = true
  error.value = null

  try {
    await useApiFetch('/parts/designators', {
      method: 'POST',
      body: form.value
    })

    toast.add({ title: 'Designator created successfully' })
    router.push('/designators')
  } catch (err: any) {
    error.value = err.data?.detail || err.message || 'Failed to create designator'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="max-w-2xl mx-auto space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold">Add New Designator</h1>
        <p class="text-gray-500 dark:text-gray-400">Create a component designator prefix.</p>
      </div>
      <UButton icon="i-heroicons-x-mark" variant="ghost" color="gray" to="/designators" />
    </div>

    <UCard>
      <div class="space-y-6 py-6">
        <UAlert v-if="error" color="error" variant="subtle" icon="i-heroicons-exclamation-circle" title="Error"
          :description="error" class="mb-4" />

        <UFormField label="Code" required help="3-character code (e.g., R for Resistor, C for Capacitor)">
          <UInput v-model="form.code" placeholder="e.g., R" maxlength="3" class="w-32 uppercase" />
        </UFormField>

        <UFormField label="Name" required>
          <UInput v-model="form.name" placeholder="e.g., Resistor" class="w-full" />
        </UFormField>
      </div>
    </UCard>

    <div class="flex items-center justify-end gap-3">
      <UButton label="Cancel" color="gray" variant="ghost" to="/designators" />
      <UButton label="Create Designator" icon="i-heroicons-plus" color="primary" :loading="isSubmitting"
        @click="handleSubmit" />
    </div>
  </div>
</template>
