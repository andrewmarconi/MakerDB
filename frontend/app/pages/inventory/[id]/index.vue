<script setup>
const route = useRoute()
const id = route.params.id

const { data: part, refresh } = await useApiFetch(`/parts/${route.params.id}`)

const tabs = [
  { label: 'Overview', icon: 'i-heroicons-information-circle' },
  { label: 'Specifications', icon: 'i-heroicons-list-bullet' },
  { label: 'Stock & Locations', icon: 'i-heroicons-circle-stack' },
  { label: 'History', icon: 'i-heroicons-clock' },
  { label: 'Attachments', icon: 'i-heroicons-paper-clip' }
]

const selectedTab = ref(0)
</script>

<template>
  <div class="space-y-6" v-if="part">
      <div class="flex items-center justify-between">
      <div class="flex items-center gap-4">
        <UButton
          variant="ghost"
          color="gray"
          icon="i-heroicons-arrow-left"
          to="/inventory"
        />
        <div>
          <h1 class="text-2xl font-bold flex items-center gap-2">
            {{ part.name }}
            <StatusBadge :status="part.type" />
          </h1>
          <div class="flex items-center gap-2 mt-1">
            <p class="text-gray-500 dark:text-gray-400 font-mono text-sm mr-2">{{ part.mpn }} • {{ part.manufacturer }}</p>
            <TagManager v-model="part.tags" />
          </div>
        </div>
      </div>
        <div class="flex items-center gap-2">
          <LabelPreview :label="part.name" :sublabel="part.mpn" :id="`PART-${part.id}`" />
          <UButton label="Edit Part" icon="i-heroicons-pencil" variant="outline" :to="`/inventory/${part.id}/edit`" />
          <StockAdjustmentModal :part="part" @saved="refresh" />
      </div>
    </div>

    <UTabs v-model="selectedTab" :items="tabs" class="w-full">
      <template #item="{ item, index }">
        <UCard v-if="index === 0" class="mt-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8 p-4">
            <div class="space-y-4">
              <h3 class="text-lg font-semibold border-b pb-2">Details</h3>
              <div class="grid grid-cols-2 gap-2 text-sm">
                <span class="text-gray-500">Manufacturer:</span> <span>{{ part.manufacturer }}</span>
                <span class="text-gray-500">MPN:</span> <span class="font-mono">{{ part.mpn }}</span>
                <span class="text-gray-500">Footprint:</span> <span class="font-mono">{{ part.footprint }}</span>
                <span class="text-gray-500">Description:</span> <span>{{ part.description }}</span>
              </div>
            </div>
            <div class="space-y-4">
              <h3 class="text-lg font-semibold border-b pb-2">Inventory Status</h3>
              <div class="flex items-center gap-8">
                <div>
                  <div class="text-sm text-gray-500">Total Stock</div>
                  <div class="text-3xl font-bold">{{ part.stock }}</div>
                </div>
                <StatusBadge status="In Stock" />
              </div>
              <div class="mt-4">
                <div class="text-sm font-medium mb-2">Stored at:</div>
                <div class="flex flex-wrap gap-2">
                  <UBadge v-for="loc in part.locations" :key="loc.name" variant="subtle" color="gray">
                    {{ loc.name }} ({{ loc.quantity }})
                  </UBadge>
                </div>
              </div>
            </div>
          </div>
        </UCard>

        <UCard v-else-if="index === 1" class="mt-4">
          <div class="p-4 space-y-8">
            <section>
              <h3 class="text-lg font-semibold mb-4">Technical Specifications</h3>
              <UTable :rows="part.specs" :columns="[{ key: 'label', label: 'Property' }, { key: 'value', label: 'Value' }]" />
            </section>
            
            <section>
              <div class="flex items-center justify-between mb-4">
                <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Custom Fields</h3>
                <UButton icon="i-heroicons-plus" variant="ghost" color="primary" label="Add Field" size="sm" />
              </div>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div v-if="part.customFields?.length" v-for="field in part.customFields" :key="field.label" class="flex justify-between p-3 bg-gray-50 dark:bg-gray-950 rounded border">
                  <span class="text-gray-500 text-sm font-medium">{{ field.label }}</span>
                  <span class="text-sm">{{ field.value }}</span>
                </div>
                <div v-else class="col-span-2 text-sm text-gray-500 italic p-4 text-center border border-dashed rounded">
                  No custom fields defined.
                </div>
              </div>
            </section>
          </div>
        </UCard>

        <UCard v-else-if="index === 2" class="mt-4">
          <!-- Stock content remains same -->
           <div class="p-4 space-y-6">
            <div class="flex items-center justify-between">
              <h3 class="text-lg font-semibold">Stock Inventory</h3>
              <UButton label="Add Location" icon="i-heroicons-plus" variant="ghost" color="gray" />
            </div>
            
            <UTable :rows="part.locations" :columns="[{ key: 'name', label: 'Location' }, { key: 'quantity', label: 'Quantity' }, { key: 'actions', label: '' }]">
              <template #name-data="{ row }">
                <div class="flex items-center gap-2">
                  <UIcon name="i-heroicons-map-pin" class="text-gray-400" />
                  <span class="font-mono">{{ row.name }}</span>
                </div>
              </template>
              <template #actions-data="{ row }">
                <UButton icon="i-heroicons-pencil" variant="ghost" color="gray" size="xs" />
              </template>
            </UTable>
          </div>
        </UCard>
        
        <UCard v-else-if="index === 4" class="mt-4">
          <div class="p-4">
            <AttachmentManager :attachments="part.attachments" />
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
  </div>
</template>
