<script setup lang="ts">
definePageMeta({
  title: 'Company Details'
})

useSeoMeta({
  title: 'Company Details',
  description: 'View company information and associated parts.'
})

const route = useRoute()
const toast = useToast()

const companyId = route.params.id as string

const { data: company, refresh } = await useApiFetch(`/core/companies/${companyId}`)

function getTypeBadge(company: any) {
  if (company.is_manufacturer && company.is_vendor) {
    return { label: 'Both', color: 'purple' as const }
  } else if (company.is_manufacturer) {
    return { label: 'Manufacturer', color: 'blue' as const }
  } else {
    return { label: 'Vendor', color: 'green' as const }
  }
}
</script>

<template>
  <div v-if="company" class="max-w-4xl mx-auto space-y-6">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-4">
        <UButton variant="ghost" color="gray" icon="i-heroicons-arrow-left" to="/companies" />
        <div>
          <h1 class="text-2xl font-bold">{{ (company as any).name }}</h1>
          <div class="flex items-center gap-2 mt-1">
            <UBadge v-bind="getTypeBadge(company)" size="sm" />
          </div>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <UButton label="Edit" icon="i-heroicons-pencil" variant="outline" :to="`/companies/${companyId}/edit`" />
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <UCard class="md:col-span-2">
        <template #header>
          <h3 class="font-semibold">Company Information</h3>
        </template>

        <div class="space-y-6 py-2">
          <div v-if="(company as any).website" class="flex items-start gap-3">
            <UIcon name="i-heroicons-globe-alt" class="w-5 h-5 text-gray-400 mt-0.5" />
            <div>
              <div class="text-sm text-gray-500">Website</div>
              <a :href="(company as any).website" target="_blank" class="text-primary-500 hover:underline">
                {{ (company as any).website }}
              </a>
            </div>
          </div>

          <div class="flex items-start gap-3">
            <UIcon name="i-heroicons-hashtag" class="w-5 h-5 text-gray-400 mt-0.5" />
            <div>
              <div class="text-sm text-gray-500">ID</div>
              <code class="text-sm font-mono">{{ companyId }}</code>
            </div>
          </div>

          <div class="flex items-start gap-3">
            <UIcon name="i-heroicons-calendar" class="w-5 h-5 text-gray-400 mt-0.5" />
            <div>
              <div class="text-sm text-gray-500">Created</div>
              <div class="text-sm">{{ new Date((company as any).created_at).toLocaleDateString() }}</div>
            </div>
          </div>

          <div v-if="(company as any).tags && (company as any).tags.length > 0" class="flex items-start gap-3">
            <UIcon name="i-heroicons-tag" class="w-5 h-5 text-gray-400 mt-0.5" />
            <div>
              <div class="text-sm text-gray-500">Tags</div>
              <div class="flex flex-wrap gap-2 mt-1">
                <UBadge v-for="tag in (company as any).tags" :key="tag" variant="subtle" size="sm">
                  {{ tag }}
                </UBadge>
              </div>
            </div>
          </div>
        </div>
      </UCard>

      <div class="space-y-6">
        <UCard v-if="(company as any).contacts && (company as any).contacts.length > 0">
          <template #header>
            <h3 class="font-semibold">Contacts</h3>
          </template>

          <div class="space-y-4 py-2">
            <div v-for="(contact, index) in (company as any).contacts" :key="index"
              class="flex items-start gap-3 p-2 rounded hover:bg-gray-50 dark:hover:bg-gray-800">
              <div class="p-1.5 bg-gray-100 dark:bg-gray-800 rounded">
                <UIcon name="i-heroicons-user" class="w-4 h-4 text-gray-500" />
              </div>
              <div class="flex-1 min-w-0">
                <div class="font-medium text-sm">{{ contact.name }}</div>
                <div v-if="contact.role" class="text-xs text-gray-500">{{ contact.role }}</div>
                <div v-if="contact.email" class="text-xs text-primary-500 truncate">
                  <a :href="`mailto:${contact.email}`">{{ contact.email }}</a>
                </div>
                <div v-if="contact.phone" class="text-xs text-gray-500">{{ contact.phone }}</div>
              </div>
            </div>
          </div>
        </UCard>

        <UCard v-else>
          <template #header>
            <h3 class="font-semibold">Contacts</h3>
          </template>

          <div class="py-8 text-center text-gray-500">
            <UIcon name="i-heroicons-users" class="w-8 h-8 mx-auto mb-2 opacity-50" />
            <p class="text-sm">No contacts added</p>
          </div>
        </UCard>
      </div>
    </div>
  </div>

  <div v-else class="flex items-center justify-center py-12">
    <UIcon name="i-heroicons-arrow-path" class="w-8 h-8 animate-spin text-gray-400" />
  </div>
</template>
