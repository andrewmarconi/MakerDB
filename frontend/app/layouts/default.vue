<template>
  <div class="flex h-screen overflow-hidden bg-gray-50 dark:bg-gray-950 text-gray-900 dark:text-gray-100 font-sans">
    <!-- Sidebar -->
    <AppSidebar />

    <!-- Main Content -->
    <div class="flex-1 flex flex-col min-w-0 overflow-hidden">
      <!-- Header -->
      <AppHeader />

      <!-- Page Content -->
      <main class="flex-1 overflow-y-auto p-4 md:p-8">
        <div class="max-w-7xl mx-auto h-full">
          <slot />
        </div>
      </main>
    </div>
  </div>
</template>

<style>
/* Custom transitions for dark mode */
html {
  transition: background-color 0.3s ease, color 0.3s ease;
}

/* Custom scrollbar for a premium feel */
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
