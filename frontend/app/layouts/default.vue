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
    to: '/inventory'
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
  <div class="flex h-screen overflow-hidden">
    <!-- Sidebar -->
    <aside class="w-64 border-r border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-900 overflow-y-auto">
      <div class="p-4">
        <h1 class="text-xl font-bold text-primary-600 dark:text-primary-400">MakerDB</h1>
      </div>
      <UNavigationMenu :links="links" orientation="vertical" class="px-2" />
    </aside>

    <!-- Main Content -->
    <main class="flex-1 flex flex-col min-w-0 overflow-hidden bg-white dark:bg-black">
      <!-- Header -->
      <header class="h-16 border-b border-gray-200 dark:border-gray-800 flex items-center justify-between px-6 shrink-0">
        <h2 class="text-lg font-semibold">Dashboard</h2>
        <div class="flex items-center gap-4">
          <UColorModeButton />
          <UAvatar src="https://avatars.githubusercontent.com/u/1024025?v=4" alt="User" />
        </div>
      </header>

      <!-- Page Content -->
      <div class="flex-1 p-6 overflow-y-auto">
        <slot />
      </div>
    </main>
  </div>
</template>
