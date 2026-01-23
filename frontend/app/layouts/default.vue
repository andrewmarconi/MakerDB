<template>
  <UDashboardGroup>
    <UDashboardSidebar collapsible>
      <template #header="{ collapsed }">
        <NuxtLink to="/" class="flex items-center justify-center w-full border-b border-gray-200 dark:border-gray-800" :class="collapsed ? 'h-16 py-2' : 'h-[--ui-header-height] py-3'">
          <img v-if="collapsed" src="/makerdb-logo-small.png" alt="MakerDB" class="h-full w-auto object-contain" />
          <img v-else src="/makerdb-logo-wide.png" alt="MakerDB" class="h-7 max-h-[48px] w-auto object-contain" />
        </NuxtLink>
      </template>

      <UNavigationMenu :items="links" orientation="vertical" class="w-full" />

      <template #footer>
        <UButton variant="ghost" color="neutral" icon="i-heroicons-cog-6-tooth" block class="justify-start px-2" />
      </template>
    </UDashboardSidebar>

    <UDashboardPanel>
      <template #header>
        <UDashboardNavbar>
          <template #left>
            <UDashboardSidebarCollapse />
            <UBreadcrumb :items="breadcrumbs" />
          </template>
          <template #right>
            <GlobalSearch />
            <UColorModeButton />
          </template>
        </UDashboardNavbar>
      </template>

      <template #body>
        <slot />
      </template>
    </UDashboardPanel>
  </UDashboardGroup>
</template>

<script setup lang="ts">
import { useStorage } from '@vueuse/core'

const route = useRoute()

const links = [
  {
    label: 'Dashboard',
    icon: 'i-heroicons-home',
    to: '/'
  },
  {
    label: 'Inventory',
    icon: 'i-heroicons-cube',
    to: '/inventory'
  },
  {
    label: 'Projects',
    icon: 'i-heroicons-briefcase',
    to: '/projects'
  },
  {
    label: 'Storage',
    icon: 'i-heroicons-map-pin',
    to: '/locations'
  },
  {
    label: 'Purchasing',
    icon: 'i-heroicons-shopping-cart',
    to: '/purchasing'
  },
    {
    label: 'Vendors',
    icon: 'i-heroicons-building-office-2',
    to: '/companies'
  }
]

const entityNameCache = useStorage('breadcrumb-entity-names', {})

const breadcrumbs = ref([])

async function fetchEntityName(path, segment, index, parts) {
  const cacheKey = `${path}`
  if (entityNameCache.value[cacheKey]) {
    return entityNameCache.value[cacheKey]
  }

  const isUuid = segment.length === 36 && /^[0-9a-f-]+$/i.test(segment)
  if (!isUuid || index === 0) {
    return null
  }

  const parentSegment = parts[index - 1]?.toLowerCase()
  let apiEndpoint = null

  if (parentSegment === 'projects') {
    apiEndpoint = `/db/projects/${segment}`
  } else if (parentSegment === 'inventory') {
    apiEndpoint = `/db/parts/${segment}`
  } else if (parentSegment === 'companies') {
    apiEndpoint = `/db/companies/${segment}`
  } else if (parentSegment === 'locations') {
    apiEndpoint = `/db/inventory/locations/${segment}`
  } else if (parentSegment === 'purchasing') {
    apiEndpoint = `/db/procurement/orders/${segment}`
  }

  if (apiEndpoint) {
    try {
      const data = await $fetch(apiEndpoint)
      const name = data.name || data.project_name || data.part_name || data.company_name || data.location_name || data.number || null
      if (name) {
        entityNameCache.value[cacheKey] = name
        return name
      }
    } catch (e) {
    }
  }

  return null
}

async function updateBreadcrumbs() {
  const parts = route.path.split('/').filter(Boolean)
  const homeBreadcrumb = { label: 'Home', to: '/', icon: 'i-heroicons-home' }

  if (parts.length === 0) {
    breadcrumbs.value = [homeBreadcrumb]
    return
  }

  const crumbs = [homeBreadcrumb]
  let currentPath = ''

  for (let i = 0; i < parts.length; i++) {
    const part = parts[i]
    currentPath += '/' + part

    const name = await fetchEntityName(currentPath, part, i, parts)
    const label = name || part.charAt(0).toUpperCase() + part.slice(1)

    crumbs.push({
      label,
      to: currentPath
    })
  }

  breadcrumbs.value = crumbs
}

watch(() => route.path, () => {
  updateBreadcrumbs()
}, { immediate: true })
</script>

<style>
html {
  transition: background-color 0.3s ease, color 0.3s ease;
}

::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: #e2e8f0;
  border-radius: 10px;
}

.dark ::-webkit-scrollbar-thumb {
  background: #1e293b;
}

::-webkit-scrollbar-thumb:hover {
  background: #cbd5e1;
}

.dark ::-webkit-scrollbar-thumb:hover {
  background: #334155;
}
</style>
