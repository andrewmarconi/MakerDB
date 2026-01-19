<script setup>
const route = useRoute()

const { data: project } = await useApiFetch(`/projects/${route.params.id}`)
const { data: bomItems } = await useApiFetch(`/projects/${route.params.id}/bom`)

const tabs = [
  { label: 'Overview', icon: 'i-heroicons-information-circle' },
  { label: 'BOM Management', icon: 'i-heroicons-list-bullet' },
  { label: 'Build History', icon: 'i-heroicons-wrench-screwdriver' },
  { label: 'Documentation', icon: 'i-heroicons-document-text' }
]

const selectedTab = ref(0)
const isImportModalOpen = ref(false)

const handleImport = () => {
  // Simulate import success
  console.log('BOM Imported')
}
</script>

<template>
  <div class="space-y-6" v-if="project">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-4">
        <UButton variant="ghost" color="gray" icon="i-heroicons-arrow-left" to="/projects" />
        <div>
          <h1 class="text-2xl font-bold flex items-center gap-2">
            {{ project.name }}
            <StatusBadge :status="project.status" />
          </h1>
          <p class="text-gray-500 dark:text-gray-400">{{ project.description }}</p>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <UButton label="Import BOM" icon="i-heroicons-arrow-up-tray" color="primary"
          @click="isImportModalOpen = true" />
        <UDropdownMenu
          :items="[[{ label: 'Export BOM', icon: 'i-heroicons-arrow-down-tray' }, { label: 'Archive Project', icon: 'i-heroicons-archive-box' }]]">
          <UButton variant="ghost" color="gray" icon="i-heroicons-ellipsis-horizontal" />
        </UDropdownMenu>
      </div>
    </div>

    <UTabs v-model="selectedTab" :items="tabs" class="w-full">
      <template #item="{ item, index }">
        <UCard v-if="index === 0" class="mt-4">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6 p-4">
            <UCard class="bg-primary-50 dark:bg-primary-900/10 border-primary-200 dark:border-primary-800">
              <div class="text-sm text-primary-600 dark:text-primary-400 font-medium">Purchase Value</div>
              <div class="text-3xl font-bold mt-1 text-primary-700 dark:text-primary-300">
                ${{ project.valuation.purchase.toFixed(2) }}
              </div>
            </UCard>

            <UCard class="bg-gray-50 dark:bg-gray-900/10">
              <div class="text-sm text-gray-500 font-medium">BOM Health</div>
              <div class="mt-2 flex items-center gap-2">
                <div class="flex-1 h-2 bg-gray-200 dark:bg-gray-800 rounded-full overflow-hidden flex">
                  <div class="bg-green-500 h-full"
                    :style="`width: ${(project.bomSummary.matched / project.bomSummary.totalItems) * 100}%`" />
                  <div class="bg-red-500 h-full"
                    :style="`width: ${(project.bomSummary.missing / project.bomSummary.totalItems) * 100}%`" />
                </div>
                <span class="text-xs text-gray-500">{{ project.bomSummary.matched }}/{{ project.bomSummary.totalItems
                  }}</span>
              </div>
            </UCard>

            <UCard class="bg-gray-50 dark:bg-gray-900/10">
              <div class="text-sm text-gray-500 font-medium">Project Status</div>
              <div class="mt-2">
                <StatusBadge :status="project.status" />
              </div>
            </UCard>
          </div>
        </UCard>

        <UCard v-else-if="index === 1" class="mt-4">
          <div class="p-4 space-y-4">
            <div class="flex items-center justify-between">
              <h3 class="text-lg font-semibold">Bill of Materials</h3>
              <div class="flex items-center gap-2">
                <UInput icon="i-heroicons-magnifying-glass" placeholder="Search BOM..." size="sm" />
                <UButton label="Auto-match Parts" icon="i-heroicons-sparkles" variant="soft" color="primary"
                  size="sm" />
              </div>
            </div>

            <BOMTable v-if="bomItems.length > 0" :items="bomItems" />

            <!-- BOM Table Empty State -->
            <div v-else
              class="flex flex-col items-center justify-center p-12 text-gray-400 border-2 border-dashed border-gray-200 dark:border-gray-800 rounded-lg">
              <UIcon name="i-heroicons-document-plus" class="w-12 h-12 mb-2 opacity-50" />
              <p>Drag and drop your CAD export CSV here to start.</p>
              <UButton label="Select File" variant="link" class="mt-2" @click="isImportModalOpen = true" />
            </div>
          </div>
        </UCard>

        <UCard v-else class="mt-4">
          <div class="flex flex-col items-center justify-center p-12 text-gray-400 italic">
            <UIcon name="i-heroicons-puzzle-piece" class="w-12 h-12 mb-2 opacity-50" />
            Section is under development...
          </div>
        </UCard>
      </template>
    </UTabs>

    <BOMImportModal v-model:isOpen="isImportModalOpen" @import="handleImport" />
  </div>
</template>
