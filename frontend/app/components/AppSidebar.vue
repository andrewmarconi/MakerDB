<script setup>
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
</script>

<template>
  <aside
    class="w-64 border-r border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-900 flex flex-col overflow-hidden">
    <div class="p-6 shrink-0">
      <NuxtLink to="/" class="flex items-center gap-2">
        <UIcon name="i-heroicons-cube-transparent" class="w-8 h-8 text-primary-600 dark:text-primary-400" />
        <h1 class="text-xl font-bold tracking-tight text-gray-900 dark:text-white">MakerDB</h1>
      </NuxtLink>
    </div>

    <div class="flex-1 overflow-y-auto px-4 py-2">
      <UNavigationMenu :items="links" orientation="vertical" class="w-full" />
    </div>

    <div class="p-4 border-t border-gray-200 dark:border-gray-800 shrink-0">
      <UButton variant="ghost" color="gray" icon="i-heroicons-cog-6-tooth" label="Settings" block
        class="justify-start px-2" />
    </div>
  </aside>
</template>
