<template>
  <UDashboardGroup>
    <UDashboardSidebar collapsible>
      <template #header>
        <NuxtLink to="/" class="flex items-center justify-center px-4 py-3 border-b border-gray-200 dark:border-gray-800">
          <img src="/makerdb-logo-wide.png" alt="MakerDB" class="h-7 max-h-[48px] w-auto object-contain" />
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
const route = useRoute()

const links = [
  {
    label: 'Dashboard',
    icon: 'i-heroicons-home',
    to: '/'
  },
  {
    label: 'Inventory',
    icon: 'i-heroicons-circle-stack',
    children: [
      {
        label: 'All Parts',
        to: '/inventory'
      },
      {
        label: 'Storage Locations',
        to: '/locations'
      },
      {
        label: 'Companies',
        to: '/companies'
      }
    ]
  },
  {
    label: 'Projects',
    icon: 'i-heroicons-briefcase',
    to: '/projects'
  },
  {
    label: 'Purchasing',
    icon: 'i-heroicons-shopping-cart',
    to: '/purchasing'
  }
]

const breadcrumbs = computed(() => {
  const parts = route.path.split('/').filter(Boolean)
  return [
    { label: 'Home', to: '/', icon: 'i-heroicons-home' },
    ...parts.map((part, index) => ({
      label: part.charAt(0).toUpperCase() + part.slice(1),
      to: '/' + parts.slice(0, index + 1).join('/')
    }))
  ]
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
