<script setup lang="ts">
definePageMeta({
  title: 'Add New Company'
})

const router = useRouter()
const toast = useToast()

const form = ref({
  name: '',
  website: '',
  is_manufacturer: true,
  is_vendor: false,
  contacts: [] as Array<{ name: string; email: string; phone: string; role: string }>
})

const newContact = ref({
  name: '',
  email: '',
  phone: '',
  role: ''
})

const isSubmitting = ref(false)
const error = ref<string | null>(null)

function addContact() {
  if (!newContact.value.name.trim()) return
  form.value.contacts.push({ ...newContact.value })
  newContact.value = { name: '', email: '', phone: '', role: '' }
}

function removeContact(index: number) {
  form.value.contacts.splice(index, 1)
}

async function handleSubmit() {
  if (!form.value.name.trim()) {
    error.value = 'Company name is required'
    return
  }

  isSubmitting.value = true
  error.value = null

  try {
    await useApiFetch('/core/companies', {
      method: 'POST',
      body: form.value
    })

    toast.add({ title: 'Company created successfully' })
    router.push('/companies')
  } catch (err: any) {
    error.value = err.data?.detail || err.message || 'Failed to create company'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="max-w-3xl mx-auto space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold">Add New Company</h1>
        <p class="text-gray-500 dark:text-gray-400">Create a manufacturer or vendor.</p>
      </div>
      <UButton icon="i-heroicons-x-mark" variant="ghost" color="gray" to="/companies" />
    </div>

    <UCard>
      <div class="space-y-6 py-6">
        <UAlert v-if="error" color="error" variant="subtle" icon="i-heroicons-exclamation-circle" title="Error"
          :description="error" class="mb-4" />

        <UFormField label="Company Name" required>
          <UInput v-model="form.name" placeholder="e.g., Texas Instruments" class="w-full" />
        </UFormField>

        <UFormField label="Website">
          <UInput v-model="form.website" placeholder="https://www.ti.com" class="w-full" />
        </UFormField>

        <div class="space-y-3">
          <label class="text-sm font-medium">Company Type</label>
          <div class="flex gap-4">
            <UCheckbox v-model="form.is_manufacturer" label="Manufacturer" />
            <UCheckbox v-model="form.is_vendor" label="Vendor/Supplier" />
          </div>
        </div>

        <UDivider />

        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="font-medium">Contacts</h3>
          </div>

          <div v-if="form.contacts.length > 0" class="space-y-2">
            <div v-for="(contact, index) in form.contacts" :key="index"
              class="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-900 rounded-lg">
              <div class="flex-1">
                <div class="font-medium">{{ contact.name }}</div>
                <div class="text-sm text-gray-500">
                  <span v-if="contact.role">{{ contact.role }}</span>
                  <span v-if="contact.email"> • {{ contact.email }}</span>
                  <span v-if="contact.phone"> • {{ contact.phone }}</span>
                </div>
              </div>
              <UButton icon="i-heroicons-trash" variant="ghost" color="red" size="xs" @click="removeContact(index)" />
            </div>
          </div>

          <p v-else class="text-sm text-gray-500 italic">No contacts added yet.</p>

          <div class="p-4 border border-dashed border-gray-200 dark:border-gray-800 rounded-lg space-y-3">
            <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300">Add Contact</h4>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
              <UInput v-model="newContact.name" placeholder="Contact name" class="w-full" />
              <UInput v-model="newContact.role" placeholder="Role (e.g., Sales Rep)" class="w-full" />
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
              <UInput v-model="newContact.email" placeholder="Email" type="email" class="w-full" />
              <UInput v-model="newContact.phone" placeholder="Phone" class="w-full" />
            </div>
            <UButton label="Add Contact" icon="i-heroicons-plus" size="sm" :disabled="!newContact.name.trim()"
              @click="addContact" />
          </div>
        </div>
      </div>
    </UCard>

    <div class="flex items-center justify-end gap-3">
      <UButton label="Cancel" color="gray" variant="ghost" to="/companies" />
      <UButton label="Create Company" icon="i-heroicons-plus" color="primary" :loading="isSubmitting"
        @click="handleSubmit" />
    </div>
  </div>
</template>
