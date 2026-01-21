<script setup lang="ts">
definePageMeta({
  title: 'Project Details'
})

useSeoMeta({
  title: 'Project Details',
  description: 'View and manage your project details and Bill of Materials.'
})

const route = useRoute()
const router = useRouter()
const toast = useToast()

const projectId = route.params.id as string

const { data: project, refresh: refreshProject } = await useApiFetch(`/projects/${projectId}`)
const { data: bomItems, refresh: refreshBOM } = await useApiFetch(`/projects/${projectId}/bom`)

const { data: availableParts } = await useApiFetch('/parts/')

const tabItems = [
  { label: 'Overview', icon: 'i-heroicons-information-circle', value: 'overview' },
  { label: 'BOM Management', icon: 'i-heroicons-list-bullet', value: 'bom' },
  { label: 'Build History', icon: 'i-heroicons-wrench-screwdriver', value: 'build' },
  { label: 'Documentation', icon: 'i-heroicons-document-text', value: 'docs' }
]

const searchQuery = ref('')
const editingItem = ref<string | null>(null)
const showAddModal = ref(false)
const isSaving = ref(false)

const editForm = ref({
  quantity: 1,
  designators: ''
})

const addForm = ref({
  partId: null as string | null,
  quantity: 1,
  designators: ''
})

const partSearchQuery = ref('')

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

const matchedCount = computed(() => {
  if (!bomItems.value) return 0
  return (bomItems.value as any[]).filter((item: any) => item.part).length
})

const totalQuantity = computed(() => {
  if (!bomItems.value) return 0
  return (bomItems.value as any[]).reduce((sum: number, item: any) => sum + (item.quantity || 0), 0)
})

const filteredParts = computed(() => {
  if (!availableParts.value) return []
  if (!partSearchQuery.value) return []
  const query = partSearchQuery.value.toLowerCase()
  return (availableParts.value as any[]).filter((part: any) =>
    part.name.toLowerCase().includes(query) ||
    part.mpn.toLowerCase().includes(query)
  )
})

const selectedPart = computed(() => {
  if (!addForm.value.partId || !availableParts.value) return null
  return (availableParts.value as any[]).find((p: any) => p.id === addForm.value.partId)
})

const canEdit = computed(() => {
  if (!project.value) return false
  const status = (project as any).status
  return status === 'draft' || status === 'active'
})

function startEdit(item: any) {
  editingItem.value = item.id
  editForm.value = {
    quantity: item.quantity,
    designators: item.designators || ''
  }
}

function cancelEdit() {
  editingItem.value = null
}

async function saveEdit(item: any) {
  if (!editingItem.value) return

  isSaving.value = true
  try {
    await useApiFetch(`/projects/${projectId}/bom/${item.id}`, {
      method: 'PUT',
      body: {
        quantity: editForm.value.quantity,
        designators: editForm.value.designators
      }
    })
    await refreshBOM()
    editingItem.value = null
    toast.add({ title: 'BOM item updated' })
  } catch (err: any) {
    toast.add({ title: 'Failed to update', description: err.message, color: 'error' })
  } finally {
    isSaving.value = false
  }
}

async function deleteItem(item: any) {
  if (!confirm(`Remove "${item.part?.name || 'this item'}" from BOM?`)) return

  try {
    await useApiFetch(`/projects/${projectId}/bom/${item.id}`, { method: 'DELETE' })
    await refreshBOM()
    toast.add({ title: 'Item removed from BOM' })
  } catch (err: any) {
    toast.add({ title: 'Failed to remove', description: err.message, color: 'error' })
  }
}

function openAddModal() {
  addForm.value = { partId: null, quantity: 1, designators: '' }
  partSearchQuery.value = ''
  showAddModal.value = true
}

function closeAddModal() {
  showAddModal.value = false
  addForm.value = { partId: null, quantity: 1, designators: '' }
}

async function addItem() {
  if (!addForm.value.partId) {
    toast.add({ title: 'Please select a part', color: 'warn' })
    return
  }

  isSaving.value = true
  try {
    await useApiFetch(`/projects/${projectId}/bom`, {
      method: 'POST',
      body: {
        part_id: addForm.value.partId,
        quantity: addForm.value.quantity,
        designators: addForm.value.designators
      }
    })
    await refreshBOM()
    closeAddModal()
    toast.add({ title: 'Item added to BOM' })
  } catch (err: any) {
    toast.add({ title: 'Failed to add item', description: err.message, color: 'error' })
  } finally {
    isSaving.value = false
  }
}

function selectPart(part: any) {
  addForm.value.partId = part.id
}

function getStatusColor(item: any) {
  if (!item.part) return 'amber'
  if (item.part?.stock_entries?.total_quantity >= item.quantity) return 'green'
  return 'yellow'
}
</script>

<template>
  <div class="space-y-6" v-if="project">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-4">
        <UButton variant="ghost" color="gray" icon="i-heroicons-arrow-left" to="/projects" />
        <div>
          <h1 class="text-2xl font-bold flex items-center gap-2">
            {{ (project as any).name }}
            <UBadge :color="(project as any).status === 'active' ? 'green' : (project as any).status === 'draft' ? 'amber' : 'gray'" size="sm">
              {{ (project as any).status }}
            </UBadge>
          </h1>
          <p class="text-gray-500 dark:text-gray-400">{{ (project as any).description || 'No description' }}</p>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <UButton label="Edit" icon="i-heroicons-pencil" variant="outline" :to="`/projects/${projectId}/edit`" />
        <UButton label="Import BOM" icon="i-heroicons-arrow-up-tray" color="primary" :to="`/projects/${projectId}/bom/import`" />
        <UDropdown-menu
          :items="[[{ label: 'Export BOM', icon: 'i-heroicons-arrow-down-tray' }, { label: 'Archive Project', icon: 'i-heroicons-archive-box' }]]">
          <UButton variant="ghost" color="gray" icon="i-heroicons-ellipsis-horizontal" />
        </UDropdown-menu>
      </div>
    </div>

    <UTabs :items="tabItems" class="w-full">
      <template #item="{ item }">
        <div v-if="item.value === 'overview'" class="space-y-6">
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

          <UCard v-if="(project as any).notes">
            <template #header>
              <h3 class="font-semibold">Notes</h3>
            </template>
            <div class="prose prose-sm dark:prose-invert max-w-none">
              {{ (project as any).notes }}
            </div>
          </UCard>
        </div>

        <div v-if="item.value === 'bom'" class="space-y-4">
          <UCard>
            <template #header>
              <div class="flex items-center justify-between">
                <h3 class="font-semibold">Bill of Materials</h3>
                <div class="flex items-center gap-2">
                  <UInput v-model="searchQuery" icon="i-heroicons-magnifying-glass" placeholder="Search..."
                    size="sm" class="w-64" />
                  <UButton v-if="canEdit" label="Add Item" icon="i-heroicons-plus" variant="soft" color="gray" size="sm" @click="openAddModal" />
                </div>
              </div>
            </template>

            <div v-if="filteredBOMItems.length > 0" class="overflow-x-auto">
              <table class="w-full text-sm">
                <thead>
                  <tr class="border-b border-gray-200 dark:border-gray-700">
                    <th class="text-left py-3 px-4 font-medium">Reference</th>
                    <th class="text-left py-3 px-4 font-medium">Part</th>
                    <th class="text-left py-3 px-4 font-medium">MPN</th>
                    <th class="text-left py-3 px-4 font-medium">Qty</th>
                    <th class="text-left py-3 px-4 font-medium">Stock</th>
                    <th class="text-right py-3 px-4 font-medium">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="item in filteredBOMItems" :key="item.id"
                    class="border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800/50">
                    <td class="py-3 px-4">
                      <span v-if="editingItem !== item.id">{{ item.designators || '-' }}</span>
                      <UInput v-else v-model="editForm.designators" size="sm" class="w-32" />
                    </td>
                    <td class="py-3 px-4">
                      <NuxtLink v-if="item.part" :to="`/inventory/${item.part.id}`"
                        class="text-primary-500 hover:underline font-medium">
                        {{ item.part.name }}
                      </NuxtLink>
                      <span v-else class="text-amber-600 font-medium">Unmatched</span>
                    </td>
                    <td class="py-3 px-4 font-mono text-gray-500">
                      {{ item.part?.mpn || '-' }}
                    </td>
                    <td class="py-3 px-4">
                      <span v-if="editingItem !== item.id">{{ item.quantity }}</span>
                      <UInput v-else v-model.number="editForm.quantity" type="number" size="sm" class="w-20" />
                    </td>
                    <td class="py-3 px-4">
                      <UBadge v-if="item.part" :color="getStatusColor(item)" size="sm">
                        {{ item.part.stock_entries?.total_quantity || 0 }}
                      </UBadge>
                      <span v-else class="text-gray-400">-</span>
                    </td>
                    <td class="py-3 px-4 text-right">
                      <div class="flex items-center justify-end gap-1">
                        <template v-if="editingItem === item.id">
                          <UButton icon="i-heroicons-check" size="xs" color="green" variant="ghost"
                            :loading="isSaving" @click="saveEdit(item)" />
                          <UButton icon="i-heroicons-x-mark" size="xs" color="gray" variant="ghost"
                            @click="cancelEdit" />
                        </template>
                        <template v-else>
                          <UButton icon="i-heroicons-pencil" size="xs" variant="ghost" color="gray"
                            @click="startEdit(item)" />
                          <UButton icon="i-heroicons-trash" size="xs" variant="ghost" color="red"
                            @click="deleteItem(item)" />
                        </template>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div v-else class="flex flex-col items-center justify-center p-12 text-gray-400">
              <UIcon name="i-heroicons-document-plus" class="w-12 h-12 mb-2 opacity-50" />
              <p>No BOM items yet.</p>
              <UButton v-if="canEdit" label="Add Item" variant="link" color="primary" class="mt-2" @click="openAddModal" />
            </div>
          </UCard>
        </div>

        <div v-if="item.value === 'build'" class="space-y-4">
          <UCard>
            <div class="flex flex-col items-center justify-center p-12 text-gray-400">
              <UIcon name="i-heroicons-wrench-screwdriver" class="w-12 h-12 mb-2 opacity-50" />
              <p>Build history will appear here.</p>
            </div>
          </UCard>
        </div>

        <div v-if="item.value === 'docs'" class="space-y-4">
          <UCard>
            <div class="flex flex-col items-center justify-center p-12 text-gray-400">
              <UIcon name="i-heroicons-document-text" class="w-12 h-12 mb-2 opacity-50" />
              <p>Project documentation will appear here.</p>
            </div>
          </UCard>
        </div>
      </template>
    </UTabs>

    <UModal v-model:open="showAddModal">
      <template #header>
        <div class="flex items-center justify-between">
          <h3 class="font-semibold">Add BOM Item</h3>
        </div>
      </template>

      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-1">Part</label>
          <UInput
            v-model="partSearchQuery"
            placeholder="Search parts..."
            icon="i-heroicons-magnifying-glass"
          />
          <div v-if="filteredParts.length > 0" class="mt-1 border rounded-lg max-h-48 overflow-y-auto">
            <button
              v-for="part in filteredParts"
              :key="part.id"
              class="w-full px-3 py-2 text-left hover:bg-gray-50 dark:hover:bg-gray-800 text-sm"
              @click="selectPart(part)">
              <div class="font-medium">{{ part.name }}</div>
              <div class="text-gray-500 text-xs">{{ part.mpn }}</div>
            </button>
          </div>
          <div v-if="selectedPart" class="mt-2 p-2 bg-green-50 dark:bg-green-900/20 rounded text-sm">
            <span class="font-medium text-green-700 dark:text-green-400">{{ selectedPart.name }}</span>
            <span class="text-gray-500 ml-2">{{ selectedPart.mpn }}</span>
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium mb-1">Quantity</label>
          <UInput v-model.number="addForm.quantity" type="number" min="1" />
        </div>

        <div>
          <label class="block text-sm font-medium mb-1">Designators</label>
          <UInput v-model="addForm.designators" placeholder="e.g., R1, C2-C5" />
        </div>
      </div>

      <template #footer>
        <div class="flex justify-end gap-2">
          <UButton variant="ghost" color="gray" @click="showAddModal = false">Cancel</UButton>
          <UButton icon="i-heroicons-plus" :loading="isSaving" @click="addItem">Add Item</UButton>
        </div>
      </template>
    </UModal>
  </div>

  <div v-else class="flex items-center justify-center py-12">
    <UIcon name="i-heroicons-arrow-path" class="w-8 h-8 animate-spin text-gray-400" />
  </div>
</template>
