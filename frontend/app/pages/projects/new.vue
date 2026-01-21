<script setup lang="ts">
import { apiPost } from '~/composables/useApiFetch'

definePageMeta({
  title: 'Create Project'
})

useSeoMeta({
  title: 'Create Project',
  description: 'Create a new project and start building your Bill of Materials.'
})

const router = useRouter()
const toast = useToast()

const form = ref({
  name: '',
  description: '',
  notes: '',
  status: 'draft',
  revision: '1.0'
})

const statusOptions = [
  { label: 'Draft', value: 'draft' },
  { label: 'Active', value: 'active' },
  { label: 'Archived', value: 'archived' }
]

const isSubmitting = ref(false)
const error = ref<string | null>(null)

async function handleSubmit() {
  if (!form.value.name.trim()) {
    error.value = 'Project name is required'
    return
  }

  isSubmitting.value = true
  error.value = null

  try {
    const response = await apiPost('/projects/', form.value)
    const projectId = (response as any)?.id
    if (projectId) {
      toast.add({ title: 'Project created successfully' })
      router.push(`/projects/${projectId}`)
    } else {
      throw new Error('No project ID returned')
    }
  } catch (err: any) {
    error.value = err.data?.detail || err.message || 'Failed to create project'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="max-w-3xl mx-auto space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold">Create Project</h1>
        <p class="text-gray-500 dark:text-gray-400">Start a new project with a Bill of Materials.</p>
      </div>
      <UButton icon="i-heroicons-x-mark" variant="ghost" color="neutral" to="/projects" />
    </div>

    <UCard>
      <div class="space-y-6 py-6">
        <UAlert v-if="error" color="error" variant="subtle" icon="i-heroicons-exclamation-circle" title="Error"
          :description="error" class="mb-4" />

        <UFormField label="Project Name" required>
          <UInput v-model="form.name" placeholder="e.g., ESP32 Weather Station" class="w-full" />
        </UFormField>

        <UFormField label="Description">
          <UTextarea v-model="form.description" placeholder="Brief description of the project..."
            class="w-full" :rows="3" />
        </UFormField>

        <UFormField label="Revision">
          <UInput v-model="form.revision" placeholder="1.0" class="w-32" />
        </UFormField>

        <UFormField label="Status">
          <URadioGroup v-model="form.status" :items="statusOptions" value-key="value" orientation="horizontal" />
        </UFormField>

        <UFormField label="Notes">
          <UTextarea v-model="form.notes" placeholder="Additional notes (Markdown supported)..."
            class="w-full" :rows="4" />
        </UFormField>
      </div>
    </UCard>

    <div class="flex items-center justify-end gap-3">
      <UButton label="Cancel" color="neutral" variant="ghost" to="/projects" />
      <UButton label="Create Project" icon="i-heroicons-plus" color="primary" :loading="isSubmitting"
        @click="handleSubmit" />
    </div>
  </div>
</template>
