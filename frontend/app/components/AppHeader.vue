<script setup>
const route = useRoute()

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

<template>
  <header
    class="h-16 border-b border-gray-200 dark:border-gray-800 flex items-center justify-between px-6 bg-white/80 dark:bg-black/80 backdrop-blur-md sticky top-0 z-10 shrink-0">
    <div class="flex items-center gap-4 min-w-0">
      <UBreadcrumb :items="breadcrumbs" />
    </div>

    <div class="flex items-center gap-4">
      <div class="hidden md:flex items-center">
        <UInput icon="i-heroicons-magnifying-glass" placeholder="Global Search..." class="w-64" shortcut="meta+k" />
      </div>

      <UColorModeButton />
    </div>
  </header>
</template>
