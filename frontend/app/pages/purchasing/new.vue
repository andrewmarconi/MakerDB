<script setup lang="ts">
import { apiPost } from '~/composables/useApiFetch'

definePageMeta({
  title: 'Create Order'
})

useSeoMeta({
  title: 'Create Order',
  description: 'Create a new purchase order.'
})

const router = useRouter()
const toast = useToast()

const form = ref({
  vendor_id: '',
  number: '',
  po_number: '',
  status: 'open',
  expected_arrival: null as string | null,
  comments: '',
  notes: ''
})

const statusOptions = [
  { label: 'Open', value: 'open' },
  { label: 'Ordered', value: 'ordered' },
  { label: 'Received', value: 'received' }
]

const { data: vendors } = await useApiFetch('/companies/?is_vendor=true')

const vendorOptions = computed(() => {
  if (!vendors.value) return []
  return (vendors.value as any[]).map(v => ({
    label: v.name,
    value: v.id
  }))
})

const isSubmitting = ref(false)
const error = ref<string | null>(null)

async function handleSubmit() {
  if (!form.value.vendor_id) {
    error.value = 'Vendor is required'
    return
  }
  if (!form.value.number.trim()) {
    error.value = 'Order number is required'
    return
  }

  isSubmitting.value = true
  error.value = null

  try {
    const response = await apiPost('/procurement/orders/', form.value)
    const orderId = (response as any)?.id
    if (orderId) {
      toast.add({ title: 'Order created successfully' })
      router.push(`/purchasing/${orderId}`)
    } else {
      throw new Error('No order ID returned')
    }
  } catch (err: any) {
    error.value = err.data?.detail || err.message || 'Failed to create order'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="max-w-3xl mx-auto space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold">Create Order</h1>
        <p class="text-gray-500 dark:text-gray-400">Create a new purchase order to track component procurement.</p>
      </div>
      <UButton icon="i-heroicons-x-mark" variant="ghost" color="neutral" to="/purchasing" />
    </div>

    <UCard>
      <div class="space-y-6 py-6">
        <UAlert v-if="error" color="error" variant="subtle" icon="i-heroicons-exclamation-circle" title="Error"
          :description="error" class="mb-4" />

        <UFormField label="Vendor" required>
          <USelectMenu
            v-model="form.vendor_id"
            :items="vendorOptions"
            value-key="value"
            placeholder="Select a vendor..."
            class="w-full"
          />
        </UFormField>

        <UFormField label="Order Number" required hint="Vendor's order/confirmation number">
          <UInput v-model="form.number" placeholder="e.g., WEB123456789" class="w-full" />
        </UFormField>

        <UFormField label="PO Number" hint="Your internal purchase order number">
          <UInput v-model="form.po_number" placeholder="e.g., PO-2026-001" class="w-full" />
        </UFormField>

        <UFormField label="Status">
          <URadioGroup v-model="form.status" :items="statusOptions" value-key="value" orientation="horizontal" />
        </UFormField>

        <UFormField label="Expected Arrival">
          <UInput v-model="form.expected_arrival" type="date" class="w-64" />
        </UFormField>

        <UFormField label="Comments">
          <UTextarea v-model="form.comments" placeholder="Order comments..." class="w-full" :rows="3" />
        </UFormField>

        <UFormField label="Notes">
          <UTextarea v-model="form.notes" placeholder="Internal notes..." class="w-full" :rows="3" />
        </UFormField>
      </div>
    </UCard>

    <div class="flex items-center justify-end gap-3">
      <UButton label="Cancel" color="neutral" variant="ghost" to="/purchasing" />
      <UButton label="Create Order" icon="i-heroicons-plus" color="primary" :loading="isSubmitting"
        @click="handleSubmit" />
    </div>
  </div>
</template>
