<script setup lang="ts">
import type { Ref } from 'vue'
import type { Attachment } from '#shared/types'

const props = defineProps({
  attachments: {
    type: Array as PropType<Attachment[]>,
    default: () => []
  },
  partId: {
    type: String,
    default: null
  }
})

const emit = defineEmits(['update:attachments'])

const toast = useToast()

const isUploading = ref(false)
const isDragging = ref(false)
const fileInputRef = ref<HTMLInputElement | null>(null)
const previewAttachment: Ref<Attachment | null> = ref(null)

const localAttachments = ref<Attachment[]>([...props.attachments]) as Ref<Attachment[]>

watch(() => props.attachments, (newAttachments) => {
  localAttachments.value = [...newAttachments]
}, { deep: true })

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
  if (contentType.includes('cad') || contentType.includes('gerber')) return 'i-heroicons-cpu-chip'
  return 'i-heroicons-document'
}

function isPreviewable(contentType: string): boolean {
  return contentType.startsWith('image/') || contentType === 'application/pdf'
}

async function handleFileUpload(files: FileList | null) {
  if (!files || files.length === 0) return
  if (!props.partId) {
    toast.add({ title: 'Cannot upload: Part not saved', color: 'warning' })
    return
  }

  isUploading.value = true

  for (const file of Array.from(files)) {
    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await $fetch<Attachment>(`/parts/${props.partId}/attachments`, {
        method: 'POST',
        body: formData
      })

      localAttachments.value.push(response)
      emit('update:attachments', localAttachments.value)
      toast.add({ title: `Uploaded ${file.name}`, icon: 'i-heroicons-check-circle' })
    } catch (err: any) {
      toast.add({ title: `Failed to upload ${file.name}`, description: err.message, color: 'error' })
    }
  }

  isUploading.value = false
  if (fileInputRef.value) fileInputRef.value.value = ''
}

async function handleDelete(attachment: Attachment) {
  if (!confirm(`Delete "${attachment.filename}"?`)) return

  try {
    await $fetch(`/parts/${props.partId}/attachments/${attachment.id}`, {
      method: 'DELETE'
    })

    localAttachments.value = localAttachments.value.filter(a => a.id !== attachment.id)
    emit('update:attachments', localAttachments.value)
    toast.add({ title: 'Attachment deleted', icon: 'i-heroicons-check-circle' })
  } catch (err: any) {
    toast.add({ title: 'Failed to delete attachment', description: err.message, color: 'error' })
  }
}

function onFileChange(e: Event) {
  const target = e.target as HTMLInputElement
  handleFileUpload(target.files)
}

function handleDrop(e: DragEvent) {
  isDragging.value = false
  handleFileUpload(e.dataTransfer?.files || null)
}

function openPreview(attachment: Attachment) {
  if (isPreviewable(attachment.content_type)) {
    previewAttachment.value = attachment
  }
}

function closePreview() {
  previewAttachment.value = null
}
</script>

<template>
  <div class="space-y-4">
    <div class="flex items-center justify-between">
      <h3 class="font-semibold">Linked Attachments</h3>
      <UButton v-if="partId" label="Upload File" icon="i-heroicons-cloud-arrow-up" color="primary" variant="soft"
        :loading="isUploading" @click="fileInputRef?.click()" />
    </div>

    <input ref="fileInputRef" type="file" multiple class="hidden" accept="*"
      @change="onFileChange" />

    <div v-if="partId" @dragover.prevent="isDragging = true" @dragleave.prevent="isDragging = false"
      @drop.prevent="handleDrop"
      class="relative border-2 border-dashed rounded-lg p-8 text-center transition-colors"
      :class="isDragging ? 'border-primary bg-primary/5' : 'border-gray-200 dark:border-gray-700'">
      <UIcon name="i-heroicons-cloud-arrow-up" class="w-12 h-12 mx-auto mb-3 text-gray-400" />
      <p class="text-gray-600 dark:text-gray-400 mb-2">
        Drag and drop files here, or click Upload
      </p>
      <p class="text-sm text-gray-500">Supports images, PDFs, datasheets, and CAD files</p>
    </div>

    <div v-if="localAttachments.length > 0" class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <UCard v-for="file in localAttachments" :key="file.id" class="group relative hover:shadow-md transition-shadow">
        <div class="flex items-center gap-3">
          <div class="p-2 bg-gray-100 dark:bg-gray-800 rounded cursor-pointer"
            @click="openPreview(file)">
            <UIcon :name="getFileIcon(file.content_type)" class="w-8 h-8"
              :class="isPreviewable(file.content_type) ? 'text-primary' : 'text-gray-500'" />
          </div>
          <div class="flex-1 min-w-0 cursor-pointer" @click="openPreview(file)">
            <div class="text-sm font-medium truncate">{{ file.filename }}</div>
            <div class="text-xs text-gray-500">{{ formatFileSize(file.size) }}</div>
          </div>
          <div class="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
            <UButton v-if="isPreviewable(file.content_type)" icon="i-heroicons-eye" variant="ghost" color="neutral"
               size="xs" @click="openPreview(file)" />
            <UButton icon="i-heroicons-arrow-down-tray" variant="ghost" color="neutral" size="xs"
               @click="navigateTo(`/db/attachments/${file.id}/download`, { external: true })" />
            <UButton icon="i-heroicons-trash" variant="ghost" color="error" size="xs" @click="handleDelete(file)" />
          </div>
        </div>
      </UCard>
    </div>

    <div v-else class="flex flex-col items-center justify-center p-12 border-2 border-dashed border-gray-200 dark:border-gray-800 rounded-lg text-gray-400">
      <UIcon name="i-heroicons-paper-clip" class="w-12 h-12 mb-2 opacity-50" />
      <p class="text-sm">No attachments yet.</p>
      <p v-if="partId" class="text-xs mt-1">Upload files to attach them to this part.</p>
    </div>

    <UModal v-model:open="previewAttachment">
      <UCard v-if="previewAttachment" class="max-w-4xl">
        <template #header>
          <div class="flex items-center justify-between">
            <h3 class="font-semibold truncate">{{ previewAttachment.filename }}</h3>
            <UButton color="neutral" variant="ghost" icon="i-heroicons-x-mark" @click="closePreview" />
          </div>
        </template>

        <div class="flex items-center justify-center min-h-[400px] bg-gray-50 dark:bg-gray-900 rounded">
          <img v-if="previewAttachment.content_type.startsWith('image/')"
            :src="`/db/attachments/${previewAttachment.id}/download`" :alt="previewAttachment.filename"
            class="max-w-full max-h-[600px] object-contain" />

          <iframe v-else-if="previewAttachment.content_type === 'application/pdf'"
            :src="`/db/attachments/${previewAttachment.id}/download`" class="w-full h-[600px]" />

          <div v-else class="text-center text-gray-500">
            <UIcon name="i-heroicons-document" class="w-16 h-16 mx-auto mb-4" />
            <p>Preview not available for this file type</p>
          </div>
        </div>

        <template #footer>
          <div class="flex justify-end gap-3">
            <UButton label="Download" icon="i-heroicons-arrow-down-tray"
              @click="navigateTo(`/db/attachments/${previewAttachment.id}/download`, { external: true })" />
          </div>
        </template>
      </UCard>
    </UModal>
  </div>
</template>
