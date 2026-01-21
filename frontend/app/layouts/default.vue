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
        <UButton variant="ghost" color="gray" icon="i-heroicons-cog-6-tooth" block class="justify-start px-2" />
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
            <UInput icon="i-heroicons-magnifying-glass" placeholder="Global Search..." class="w-64" shortcut="meta+k" />
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

<script setup>
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

async function fetchEntityName(path, segment, index) {
  const cacheKey = `${path}`
  if (entityNameCache.value[cacheKey]) {
    return entityNameCache.value[cacheKey]
  }

  const segmentLower = segment.toLowerCase()
  let apiEndpoint = null

  if (segmentLower === 'projects' && index < route.path.split('/').length - 1) {
    const nextSegment = route.path.split('/')[index + 1]
    if (nextSegment && nextSegment.length === 36) {
      apiEndpoint = `/db/projects/${nextSegment}`
    }
  } else if (segmentLower === 'inventory' && index < route.path.split('/').length - 1) {
    const nextSegment = route.path.split('/')[index + 1]
    if (nextSegment && nextSegment.length === 36) {
      apiEndpoint = `/db/parts/${nextSegment}`
    }
  } else if (segmentLower === 'companies' && index < route.path.split('/').length - 1) {
    const nextSegment = route.path.split('/')[index + 1]
    if (nextSegment && nextSegment.length === 36) {
      apiEndpoint = `/db/companies/${nextSegment}`
    }
  } else if (segmentLower === 'locations' && index < route.path.split('/').length - 1) {
    const nextSegment = route.path.split('/')[index + 1]
    if (nextSegment && nextSegment.length === 36) {
      apiEndpoint = `/db/locations/${nextSegment}`
    }
  } else if (segmentLower === 'purchasing' && index < route.path.split('/').length - 1) {
    const nextSegment = route.path.split('/')[index + 1]
    if (nextSegment && nextSegment.length === 36) {
      apiEndpoint = `/db/orders/${nextSegment}`
    }
  }

  if (apiEndpoint) {
    try {
      const data = await $fetch(apiEndpoint)
      const name = data.name || data.project_name || data.part_name || data.company_name || data.location_name || null
      if (name) {
        entityNameCache.value[cacheKey] = name
        return name
      }
    } catch (e) {
    }
  }

  return null
}

const breadcrumbs = computed(async () => {
  const parts = route.path.split('/').filter(Boolean)
  const homeBreadcrumb = { label: 'Home', to: '/', icon: 'i-heroicons-home' }

  if (parts.length === 0) return [homeBreadcrumb]

  const breadcrumbs = [homeBreadcrumb]
  let currentPath = ''

  for (let i = 0; i < parts.length; i++) {
    const part = parts[i]
    currentPath += '/' + part

    const name = await fetchEntityName(currentPath, part, i)
    const label = name || part.charAt(0).toUpperCase() + part.slice(1)

    breadcrumbs.push({
      label,
      to: currentPath
    })
  }

  return breadcrumbs
})
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
