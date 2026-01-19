<script setup>
const props = defineProps({
  attachments: {
    type: Array,
    default: () => []
  }
})

const items = ref([...props.attachments])

const handleUpload = () => {
  // Simulate file upload
  const newFile = {
    id: Date.now(),
    name: 'Datasheet_Rev_B.pdf',
    size: '1.2 MB',
    type: 'application/pdf',
    date: new Date().toISOString().split('T')[0]
  }
  items.value.push(newFile)
}

const deleteFile = (id) => {
  items.value = items.value.filter(f => f.id !== id)
}
</script>

<template>
  <div class="space-y-4">
    <div class="flex items-center justify-between">
      <h3 class="font-semibold">Linked Attachments</h3>
      <UButton label="Upload File" icon="i-heroicons-cloud-arrow-up" color="primary" variant="soft" @click="handleUpload" />
    </div>

    <div v-if="items.length > 0" class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <UCard v-for="file in items" :key="file.id" class="group relative">
        <div class="flex items-center gap-3">
          <div class="p-2 bg-gray-100 dark:bg-gray-800 rounded">
            <UIcon :name="file.type.includes('pdf') ? 'i-heroicons-document-text' : 'i-heroicons-photo'" class="w-8 h-8 text-gray-500" />
          </div>
          <div class="flex-1 min-w-0">
            <div class="text-sm font-medium truncate">{{ file.name }}</div>
            <div class="text-xs text-gray-500">{{ file.size }} • {{ file.date }}</div>
          </div>
          <div class="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
            <UButton icon="i-heroicons-eye" variant="ghost" color="gray" size="xs" />
            <UButton icon="i-heroicons-trash" variant="ghost" color="red" size="xs" @click="deleteFile(file.id)" />
          </div>
        </div>
      </UCard>
    </div>

    <div v-else class="flex flex-col items-center justify-center p-12 border-2 border-dashed border-gray-200 dark:border-gray-800 rounded-lg text-gray-400">
      <UIcon name="i-heroicons-paper-clip" class="w-12 h-12 mb-2 opacity-50" />
      <p class="text-sm">No attachments found.</p>
      <UButton label="Click to upload" variant="link" @click="handleUpload" />
    </div>
  </div>
</template>
