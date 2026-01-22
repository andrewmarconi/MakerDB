<script setup lang="ts">
import type { FieldSchema } from '~/shared/types/ui'
import DataFormView from '~/components/DataFormView.vue'
import DataFormInlineView from '~/components/DataFormInlineView.vue'

definePageMeta({
  title: 'Project Details'
})

useSeoMeta({
  title: 'Project Details',
  description: 'View and manage your project details and Bill of Materials.'
})

const route = useRoute()
const toast = useToast()

const projectId = route.params.id as string

const { data: project, refresh: refreshProject } = await useApiFetch(`/projects/${projectId}`)
const { data: bomItems, refresh: refreshBOM } = await useApiFetch(`/projects/${projectId}/bom`)
const { data: attachments, refresh: refreshAttachments } = await useApiFetch(`/projects/${projectId}/attachments`)

const tabs = [
  { label: 'Details', icon: 'i-heroicons-information-circle', value: 'details', slot: 'details' },
  { label: 'Bill of Materials', icon: 'i-heroicons-list-bullet', value: 'bom', slot: 'bom' },
  { label: 'Attachments', icon: 'i-heroicons-paper-clip', value: 'attachments', slot: 'attachments' },
]

const activeTab = ref('details')

const bomFormRef = ref()

function initBOMAddForm() {
  if (bomFormRef.value) {
    bomFormRef.value.initNewItemForm()
  }
}

const searchQuery = ref('')

const matchedCount = computed(() => {
  if (!bomItems.value) return 0
  return (bomItems.value as any[]).filter((item: any) => item.part).length
})

const totalQuantity = computed(() => {
  if (!bomItems.value) return 0
  return (bomItems.value as any[]).reduce((sum: number, item: any) => sum + (item.quantity || 0), 0)
})

const filteredBOMItems = computed(() => {
  if (!bomItems.value) return []
  if (!searchQuery.value) return bomItems.value
  const query = searchQuery.value.toLowerCase()
  return (bomItems.value as any[]).filter((item: any) =>
    item.part?.name?.toLowerCase().includes(query) ||
    item.part?.mpn?.toLowerCase().includes(query) ||
    item.designators?.toLowerCase().includes(query)
  )
})

const canEdit = computed(() => {
  if (!project.value) return false
  const status = (project as any).status
  return status === 'draft' || status === 'active'
})

const detailsSchema: FieldSchema[] = [
  { key: 'name', label: 'Project Name', type: 'text', required: true, span: 2 },
  { key: 'revision', label: 'Revision', type: 'text', span: 1 },
  { key: 'status', label: 'Status', type: 'select', options: [
    { label: 'Draft', value: 'draft' },
    { label: 'Active', value: 'active' },
    { label: 'Archived', value: 'archived' },
  ], span: 1 },
  { key: 'description', label: 'Description', type: 'textarea', span: 2 },
  { key: 'notes', label: 'Notes', type: 'textarea', span: 2 },
]

const bomItemSchema: FieldSchema[] = [
  { key: 'part_id', label: 'Part', type: 'search', searchEndpoint: '/parts/search', searchLabelKey: 'name', searchQueryParam: 'q', required: true },
  { key: 'quantity', label: 'Qty', type: 'number', required: true },
  { key: 'designators', label: 'Reference', type: 'text' },
]

const bomDisplayColumns = [
  {
    key: 'mpn',
    label: 'MPN',
    render: (item: any) => {
      if (!item.part?.mpn) return '-'
      return h('span', { class: 'font-mono text-gray-500 text-sm' }, item.part.mpn)
    }
  },
  {
    key: 'stock',
    label: 'Stock',
    render: (item: any) => {
      if (!item.part) return '-'
      const hasStock = (item.part.stock_entries?.total_quantity || 0) >= item.quantity
      const color = hasStock ? 'success' : 'warning'
      const count = item.part.stock_entries?.total_quantity || 0
      return h(UBadge, { color, size: 'sm', variant: 'subtle' }, () => count)
    }
  },
]

async function handleSave(field: string, value: any, response: any) {
  toast.add({ title: `${field} updated`, icon: 'i-heroicons-check-circle' })
  if (response) {
    project.value = response
  }
  await refreshProject()
}

function handleSaveError(field: string, error: Error) {
  toast.add({ title: `Failed to update ${field}`, description: error.message, color: 'error' })
}

async function handleBOMAdded(item: any) {
  toast.add({ title: 'Component added to BOM' })
  await refreshBOM()
}

async function handleBOMUpdated(item: any) {
  toast.add({ title: 'BOM item updated' })
  await refreshBOM()
}

async function handleBOMDeleted(id: string) {
  toast.add({ title: 'Item removed from BOM' })
  await refreshBOM()
}

async function handleBOMRefresh() {
  await refreshBOM()
}

const isUploading = ref(false)
const fileInputRef = ref<HTMLInputElement | null>(null)

function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

function getFileIcon(contentType: string): string {
  if (contentType.startsWith('image/')) return 'i-heroicons-photo'
  if (contentType === 'application/pdf') return 'i-heroicons-document-text'
  return 'i-heroicons-document'
}

function isPreviewable(contentType: string): boolean {
  return contentType.startsWith('image/') || contentType === 'application/pdf'
}

async function handleFileUpload(files: FileList | null) {
  if (!files || files.length === 0) return

  isUploading.value = true

  for (const file of Array.from(files)) {
    try {
      const formData = new FormData()
      formData.append('file', file)

      await $fetch(`/projects/${projectId}/attachments`, {
        method: 'POST',
        body: formData
      })

      toast.add({ title: `Uploaded ${file.name}`, icon: 'i-heroicons-check-circle' })
      await refreshAttachments()
    } catch (err: any) {
      toast.add({ title: `Failed to upload ${file.name}`, description: err.message, color: 'error' })
    }
  }

  isUploading.value = false
  if (fileInputRef.value) fileInputRef.value.value = ''
}

function onFileChange(e: Event) {
  const target = e.target as HTMLInputElement
  handleFileUpload(target.files)
}

async function handleDeleteAttachment(attachment: any) {
  if (!confirm(`Delete "${attachment.filename}"?`)) return

  try {
    await $fetch(`/projects/${projectId}/attachments/${attachment.id}`, { method: 'DELETE' })
    toast.add({ title: 'Attachment deleted', icon: 'i-heroicons-check-circle' })
    await refreshAttachments()
  } catch (err: any) {
    toast.add({ title: 'Failed to delete attachment', description: err.message, color: 'error' })
  }
}

function downloadAttachment(attachment: any) {
  navigateTo(`/db/attachments/${attachment.id}/download`, { external: true })
}
</script>

<template>
  <div class="space-y-6" v-if="project">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-4">
        <UButton variant="ghost" color="neutral" icon="i-heroicons-arrow-left" to="/projects" />
        <div>
          <h1 class="text-2xl font-bold flex items-center gap-2">
            {{ (project as any).name }}
            <UBadge :color="(project as any).status === 'active' ? 'success' : (project as any).status === 'draft' ? 'warning' : 'neutral'" size="sm">
              {{ (project as any).status }}
            </UBadge>
          </h1>
          <p class="text-gray-500 dark:text-gray-400">{{ (project as any).description || 'No description' }}</p>
        </div>
      </div>
    </div>

    <UTabs v-model="activeTab" :items="tabs" class="w-full">
      <template #details>
        <UCard>
          <template #header>
            <div class="flex items-center justify-between">
              <h3 class="font-semibold">Project Details</h3>
              <UBadge variant="subtle" color="neutral">
                <UIcon name="i-heroicons-pencil" class="w-3 h-3 mr-1" />
                Click any field to edit
              </UBadge>
            </div>
          </template>

          <DataFormView
            v-model="project"
            :schema="detailsSchema"
            endpoint="/projects"
            :entity-id="projectId"
            save-mode="put"
            layout="two-column"
            @save="handleSave"
            @save-error="handleSaveError"
          />
        </UCard>

        <UCard class="mt-4">
          <template #header>
            <h3 class="font-semibold">Overview</h3>
          </template>

          <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <UCard>
              <div class="text-sm text-gray-500">BOM Items</div>
              <div class="text-2xl font-bold mt-1">{{ bomItems?.length || 0 }}</div>
            </UCard>
            <UCard>
              <div class="text-sm text-gray-500">Total Quantity</div>
              <div class="text-2xl font-bold mt-1">{{ totalQuantity }}</div>
            </UCard>
            <UCard>
              <div class="text-sm text-gray-500">Matched Parts</div>
              <div class="text-2xl font-bold mt-1 text-green-600">{{ matchedCount }}</div>
            </UCard>
            <UCard>
              <div class="text-sm text-gray-500">Revision</div>
              <div class="text-2xl font-bold mt-1">{{ (project as any).revision || '1.0' }}</div>
            </UCard>
          </div>
        </UCard>
      </template>

      <template #bom>
        <div class="space-y-4">
          <div class="flex justify-end">
            <UButton
              label="New Component"
              icon="i-heroicons-plus"
              color="primary"
              size="sm"
              @click="initBOMAddForm"
            />
          </div>
          <DataFormInlineView
            ref="bomFormRef"
            :items="filteredBOMItems"
            :item-schema="bomItemSchema"
            :display-columns="bomDisplayColumns"
            :base-endpoint="`/projects/${projectId}/bom`"
            :can-edit="canEdit"
            empty-state-message="No BOM items yet. Add components or import a BOM."
            @item-added="handleBOMAdded"
            @item-updated="handleBOMUpdated"
            @item-deleted="handleBOMDeleted"
            @refresh="handleBOMRefresh"
          />
        </div>
      </template>

      <template #attachments>
        <UCard>
          <template #header>
            <div class="flex items-center justify-between">
              <h3 class="font-semibold">Attachments</h3>
              <UButton label="Upload File" icon="i-heroicons-cloud-arrow-up" color="primary" variant="soft" :loading="isUploading" @click="fileInputRef?.click()" />
            </div>
          </template>

          <input ref="fileInputRef" type="file" multiple class="hidden" @change="onFileChange" />

          <div v-if="attachments && (attachments as any[]).length > 0" class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <UCard v-for="file in attachments" :key="file.id" class="group relative hover:shadow-md transition-shadow">
              <div class="flex items-center gap-3">
                <div class="p-2 bg-gray-100 dark:bg-gray-800 rounded cursor-pointer" @click="isPreviewable(file.content_type) && navigateTo(`/db/attachments/${file.id}/download`, { external: true })">
                  <UIcon :name="getFileIcon(file.content_type)" class="w-8 h-8" :class="isPreviewable(file.content_type) ? 'text-primary' : 'text-gray-500'" />
                </div>
                <div class="flex-1 min-w-0 cursor-pointer" @click="navigateTo(`/db/attachments/${file.id}/download`, { external: true })">
                  <div class="text-sm font-medium truncate">{{ file.filename }}</div>
                  <div class="text-xs text-gray-500">{{ formatFileSize(file.size) }}</div>
                </div>
                <div class="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                  <UButton icon="i-heroicons-arrow-down-tray" variant="ghost" color="neutral" size="xs" @click="downloadAttachment(file)" />
                  <UButton icon="i-heroicons-trash" variant="ghost" color="error" size="xs" @click="handleDeleteAttachment(file)" />
                </div>
              </div>
            </UCard>
          </div>

          <div v-else class="flex flex-col items-center justify-center p-12 border-2 border-dashed border-gray-200 dark:border-gray-800 rounded-lg text-gray-400">
            <UIcon name="i-heroicons-paper-clip" class="w-12 h-12 mb-2 opacity-50" />
            <p class="text-sm">No attachments yet.</p>
            <p class="text-xs mt-1">Upload files to attach them to this project.</p>
          </div>
        </UCard>
      </template>
    </UTabs>
  </div>

  <div v-else class="flex items-center justify-center py-12">
    <UIcon name="i-heroicons-arrow-path" class="w-8 h-8 animate-spin text-gray-400" />
  </div>
</template>
