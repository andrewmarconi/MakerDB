<script setup lang="ts">
definePageMeta({
  title: 'Edit Project'
})

useSeoMeta({
  title: 'Edit Project',
  description: 'Edit your project details and settings.'
})

const route = useRoute()
const router = useRouter()
const toast = useToast()

const projectId = route.params.id as string

const { data: project, refresh } = await useApiFetch(`/projects/${projectId}`)

const form = ref({
  name: '',
  description: '',
  notes: '',
  status: 'draft',
  revision: '1.0'
})

watch(project, (newProject) => {
  if (newProject) {
    form.value.name = (newProject as any).name || ''
    form.value.description = (newProject as any).description || ''
    form.value.notes = (newProject as any).notes || ''
    form.value.status = (newProject as any).status || 'draft'
    form.value.revision = (newProject as any).revision || '1.0'
  }
}, { immediate: true })

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
    await useApiFetch(`/projects/${projectId}`, {
      method: 'PUT',
      body: form.value
    })

    toast.add({ title: 'Project updated successfully' })
    router.push(`/projects/${projectId}`)
  } catch (err: any) {
    error.value = err.data?.detail || err.message || 'Failed to update project'
  } finally {
    isSubmitting.value = false
  }
}

async function handleDelete() {
  if (!confirm('Are you sure you want to delete this project?')) return

  try {
    await useApiFetch(`/projects/${projectId}`, { method: 'DELETE' })
    toast.add({ title: 'Project deleted' })
    router.push('/projects')
  } catch (err: any) {
    toast.add({ title: 'Failed to delete project', description: err.message, color: 'error' })
  }
}
</script>

<template>
  <div v-if="project" class="max-w-3xl mx-auto space-y-6">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-4">
        <UButton variant="ghost" color="gray" icon="i-heroicons-arrow-left" :to="`/projects/${projectId}`" />
        <div>
          <h1 class="text-2xl font-bold">Edit Project</h1>
          <p class="text-gray-500 dark:text-gray-400">Update project details.</p>
        </div>
      </div>
      <UButton icon="i-heroicons-trash" label="Delete" variant="ghost" color="red" @click="handleDelete" />
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
      <UButton label="Cancel" color="gray" variant="ghost" :to="`/projects/${projectId}`" />
      <UButton label="Save Changes" icon="i-heroicons-check" color="primary" :loading="isSubmitting"
        @click="handleSubmit" />
    </div>
  </div>

  <div v-else class="flex items-center justify-center py-12">
    <UIcon name="i-heroicons-arrow-path" class="w-8 h-8 animate-spin text-gray-400" />
  </div>
</template>
